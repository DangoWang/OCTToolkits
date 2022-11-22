thrift.exe --gen py -o %cd% -v rpc_schema.thrift
xcopy gen-py . /s /y
pause