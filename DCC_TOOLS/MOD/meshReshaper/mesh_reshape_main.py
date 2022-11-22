#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Dango Wang
# time : 2019/3/20

import os
import logging
import sys
import maya.cmds as mc
import maya.mel as mel
import pymel.core as pm
import numpy
import heapq
import loadUiType
from double_circle_link_list import *
from PySide2 import QtCore


def undoable(function):
    """A decorator that will make commands undoable in maya"""
    def decoratorCode(*args, **kwargs):
        mc.undoInfo(openChunk=True)
        functionReturn = None
        try:
            functionReturn = function(*args, **kwargs)
        except:
            print sys.exc_info()[1]

        finally:
            mc.undoInfo(closeChunk=True)
            return functionReturn
    return decoratorCode


def delete_not_bound_edges(pm_shape):
    for _ in xrange(5):
        for each in pm_shape.e:
            if not each.isOnBoundary():
                pm.delete(each)
    return


def get_plane_center(pm_shape):
    return numpy.array(pm_shape.getPoints(space='world')).mean(0).tolist()


def get_distance_list(pm_shape, center):
    distance_list = []
    for edge in pm_shape.e:
        edge_point = edge.getPoint(0)
        edge_pos_array = numpy.array(edge_point)
        distance_ = numpy.linalg.norm(edge_pos_array - center)
        dict_temp = {"distance": distance_, "edge": edge}
        distance_list.append(dict_temp)
    return distance_list


def get_internal_edges(pm_shape, distance_list, edges_num):
    further = heapq.nlargest(edges_num, distance_list, key=lambda s: s['distance'])
    internal_edges = [ed for ed in pm_shape.e if ed not in [j['edge'] for j in further]]
    return internal_edges


def get_internal_crv(pm_plane_shape, edges_num, rebuild_num):
    delete_not_bound_edges(pm_plane_shape)
    plane_center = get_plane_center(pm_plane_shape)
    distance_list = get_distance_list(pm_plane_shape, plane_center)
    internal_edges = get_internal_edges(pm_plane_shape, distance_list, edges_num)
    if not internal_edges:
        return False
    pm.select(internal_edges, r=True)
    internal_crv = pm.PyNode(mel.eval('polyToCurve -form 2 -degree 3;')[0]).getShape()
    # pm.rebuildCurve(internal_crv, rpo=1, ch=1, end=1, kr=0, kcp=0, kt=0, d=3, tol=0.01, rt=0, s=rebuild_num)
    transform_ = pm_plane_shape.getParent()
    # pm.rebuildCurve(transform_, rpo=1, ch=1, end=1, kr=0, kcp=0, kt=0, d=3, tol=0.01, rt=0, s=rebuild_num)
    pm.delete(transform_)
    return internal_crv


def get_points_on_crv_pos(pm_crv_shape):
    points_pos_list = []
    all_jnts = list()
    for each in pm_crv_shape.cv:
        points_pos_list.append(each.getPosition(space='world'))
    for p in points_pos_list:
        joint_ = mc.joint(p=p)
        jnt_pynode = pm.PyNode(joint_)
        jnt_pynode_p = jnt_pynode.getParent()
        if pm.nodeType(jnt_pynode_p) == 'joint':
            mc.joint(jnt_pynode_p.name(), e=1, zso=1, oj='yxz', sao='yup')
        all_jnts.append(joint_)
    return all_jnts


def create_a_plane(foot_name, edges_num, jnt):
    plane = mel.eval('polyPlane -n {}_poly_plane -w 1 -h 1 -sx {} -sy {} -ax 0 1 0 -cuv 2 -ch 1;'
                     .format(foot_name, edges_num, edges_num))
    mc.parentConstraint(jnt, plane)
    return plane


def create_planes(foot_name, edges_num, jnts):
    for each_jnt in jnts:
        plane = create_a_plane(foot_name, edges_num, each_jnt)
        pm.select(plane, add=1)
        yield plane
    # for each_pos in pos:
    #     create_a_plane(foot_name, edges_num, each_pos)


def extract_a_curve(pm_mesh, plane, edges_num, rebuild_num):
    new_mesh = pm.duplicate(pm_mesh, rr=1)
    try:
        c = pm.polyCBoolOp(plane, new_mesh, op=2, ch=1, preserveColor=0, classification=2)[0]
    except:
        return False
    pm.select(c, r=True)
    mel.eval('DeleteHistory;')
    pm.delete(new_mesh)
    the_internal_crv = get_internal_crv(c.getShape(), edges_num, rebuild_num)
    if not the_internal_crv:
        return False
    return the_internal_crv


def extract_curves(pm_mesh, planes, edges_num, rebuild_num):
    pm.select(cl=1)
    for each in planes:
        crv = extract_a_curve(pm_mesh, each, edges_num, rebuild_num)
        if crv:
            pm.select(crv, add=1)
            yield crv
        else:
            continue


def make_crv_to_circle(pos, rebuild_num, radius, crv_shape):
    circle_temp = pm.circle(c=pos, nr=[0, 1, 0], r=radius)[0]
    circle_temp_shape = circle_temp.getShape()
    pm.rebuildCurve(circle_temp_shape, rpo=1, ch=1, end=1, kr=0, kcp=0, kt=0, d=3, tol=0.01, rt=0, s=rebuild_num)
    all_cv_temp = circle_temp_shape.getCVs()
    crv_shape.setCVs(all_cv_temp)
    # pm.delete(circle_temp)
    return crv_shape


def make_crvs_to_circles(rebuild_num, radius, crv_shapes):
    y = 0
    for each in crv_shapes:
        crv = make_crv_to_circle(pos=[0, y, 0], rebuild_num=rebuild_num, radius=radius, crv_shape=each)
        y += 0.5
        yield crv


file_path = str(os.path.split(os.path.realpath(__file__))[0])
form_class, base_class = loadUiType.loadUiType(file_path+'/mesh_reshape_ui.ui')


class MeshReshape(base_class, form_class):
    def __init__(self):
        super(MeshReshape, self).__init__(parent=loadUiType.getMayaWindow())
        self.setupUi(self)

    @QtCore.Slot(name='on_foot_pb_clicked')
    def on_foot_pb_clicked(self):
        selected = mc.ls(sl=1)
        if not selected:
            logging.error(u'请先选择物体！')
            return False
        self.foot_le.setText(selected[0])
        return selected[0]

    @property
    def foot_name(self):
        if not self.foot_le.text():
            logging.error(u'请填入触角名称！')
            return ""
        return pm.PyNode(self.foot_le.text())

    @property
    def rebuild_crv_num(self):
        return self.rebuild_crv_sb.value()

    @property
    def cv_offset(self):
        return self.cv_offset_sb.value()

    @property
    def rebuild_crv_2_num(self):
        return self.rebuild_crv_2_sb.value()

    @property
    def plane_edges_num(self):
        return self.make_planes_sb.value()

    @property
    def cylinder_radius(self):
        return self.build_cylinder_sb.value()

    @QtCore.Slot(name='on_rebuild_crv_pb_clicked')
    @undoable
    def on_rebuild_crv_pb_clicked(self):
        selected = mc.ls(sl=1)
        if not selected:
            logging.error(u'请选择曲线！')
            return False
        for each in selected:
            mc.rebuildCurve(each, rpo=1, ch=1, end=1, kr=0, kcp=0, kt=0, d=3, tol=0.01, rt=0, s=self.rebuild_crv_num)
        return True

    @QtCore.Slot(name='on_make_planes_pb_clicked')
    @undoable
    def on_make_planes_pb_clicked(self):
        selected = pm.ls(sl=1)
        if not selected:
            logging.error(u'请选择曲线！')
            return False
        points_on_crv_jnts = get_points_on_crv_pos(selected[0])
        cp = create_planes(self.foot_name, self.plane_edges_num, points_on_crv_jnts)
        planes = []
        while True:
            try:
                planes.append(cp.next()[0])
            except:
                break
        mc.delete(mc.group(points_on_crv_jnts))
        pm.group(planes, name=self.foot_name+'_polyPlanes_grp')
        pm.select(planes, r=1)
        # create_planes(self.foot_name, self.plane_edges_num, points_on_crv_pos)
        return

    @QtCore.Slot(name='on_make_loft_crvs_pb_clicked')
    @undoable
    def on_make_loft_crvs_pb_clicked(self):
        plane_grp = self.foot_name+'_polyPlanes_grp'
        if not mc.objExists(plane_grp):
            return False
        all_planes = pm.listRelatives(plane_grp, c=1, ad=1, s=1)
        ec = extract_curves(self.foot_name, all_planes, self.plane_edges_num*4, rebuild_num=self.rebuild_crv_2_num)
        all_crvs = []
        while True:
            try:
                all_crvs.append(all_crvs.append(ec.next()))
            except:
                break
        pm.select(all_crvs, r=True)
        self.on_rebuild_crv_pb_clicked()
        pm.group(all_crvs, name=self.foot_name+'_loft_crvs')
        return

    @QtCore.Slot(name='on_reshape_mesh_pb_clicked')
    def on_reshape_mesh_pb_clicked(self):
        loft_crvs = self.foot_name+'_loft_crvs'
        all_crvs = pm.listRelatives(loft_crvs, c=1)
        pm.loft(all_crvs, ch=1, u=1, c=0, ar=1, d=1, ss=1, rn=0, po=1, rsn=True)

    @QtCore.Slot(name='on_cv_offset_pb_clicked')
    @undoable
    def on_cv_offset_pb_clicked(self):
        selected = pm.ls(sl=1)
        if not selected:
            logging.error(u'请选择曲线！')
            return False
        for each in selected:
            crv_shape = each.getShape()
            all_cvs = crv_shape.getCVs(space='world')
            crv_double_link_list = DoubleCircleLinkList()
            for j in xrange(len(crv_shape.cv)):
                crv_double_link_list.append(all_cvs[j])
            new_cvs = crv_double_link_list.get_items(start_index=self.cv_offset)
            for index, cv in enumerate(crv_shape.cv):
                cv.setPosition(new_cvs[index], space='world')
            # crv_shape.setCVs(new_cvs, space='world')
            mel.eval('move -r -os -wd 0 1 0 ;')
            mel.eval('undo;')
        return True

    @QtCore.Slot(name='on_build_cylinder_pb_clicked')
    @undoable
    def on_build_cylinder_pb_clicked(self):
        loft_crvs_grp = self.foot_name + '_loft_crvs'
        new_grp_temp = pm.duplicate(loft_crvs_grp, rr=1, name=self.foot_name+'_cylinder_loft_crvs')
        all_new_crvs = pm.listRelatives(new_grp_temp, c=1, ad=1, s=1)
        circles = make_crvs_to_circles(rebuild_num=self.rebuild_crv_2_num,
                                       radius=self.cylinder_radius,
                                       crv_shapes=all_new_crvs)
        while True:
            try:
                circles.next()
            except:
                break
        pm.loft(pm.listRelatives(new_grp_temp, c=1), ch=1, u=1, c=0, ar=1, d=1, ss=1, rn=0, po=1, rsn=True)
        return True





