namespace py rpc_schema

service OCT_RPC{
    string hello(),
    bool aliyun_upload(1:string file_list_data),
    bool aliyun_download(1:string file_list_data),
    binary call_sg(1:string mode, 2:binary data),
    string sg_download_attachment(1:binary sg_file_info),
}
