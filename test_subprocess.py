# import subprocess
# # proc = subprocess.Popen(['python3', '-i'],
# #                             stdin=subprocess.PIPE,
# #                             stdout=subprocess.PIPE,
# #                             stderr=subprocess.PIPE)
#
# from subprocess import Popen, PIPE, STDOUT
# subprocess.run(['node /Users/renpeng/Downloads/node_modules/bilibili-live-danmaku-api/stdio.js'], input='1502a8ee%2C1571610493%2C60b13f91 5524c8c121497774904472148b122504 686555 hello'.encode('utf-8'), shell=True)
# # p = Popen(['/Users/renpeng/Downloads/node_modules/bilibili-live-danmaku-api/stdio.js'], stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
# # stdout_data = p.communicate(input=bytes('data_to_write', encoding='utf8'))[0]

# from Naked.toolshed.shell import execute_js, muterun_js
# import time
# start_time = time.time()
# success = execute_js('./bilibili-live-danmaku-api/stdio.js 1502a8ee%2C1571610493%2C60b13f91 5524c8c121497774904472148b122504 686555 test')
# print("---generation process cost %s seconds ---" % (time.time() - start_time))

#! /usr/bin/env python
# import subprocess
# import time
# for _ in range(3):
#     start_time = time.time()
#     subprocess.call('sudo node ./bilibili-live-danmaku-api/stdio.js 1502a8ee%2C1571610493%2C60b13f91 5524c8c121497774904472148b122504 686555 test', shell=True)
#     print("---generation process cost %s seconds ---" % (time.time() - start_time))

# from datetime import datetime
# from socketIO_client import SocketIO, LoggingNamespace
# import sys
#
# while True:
#     with SocketIO( 'localhost', 3000, LoggingNamespace ) as socketIO:
#         now = datetime.now()
#         socketIO.emit( 'python-message', now.strftime( "%-d %b %Y %H:%M:%S.%f" ) )
#         socketIO.wait( seconds=1 )

import pdb

def not_removed(single):
    char_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    use_this_one = False
    single = single.lower()
    for character in single:
        if (character not in char_list) and (not character.isdigit()):
            use_this_one = True
    if single in ['kksk', 'awsl', 'rua']:
        use_this_one = True
    return use_this_one

not_removed('哈哈')
pdb.set_trace()
pdb.set_trace()


# import requests
# import json
# import pdb
#
# url = "http://localhost:3000"
# data = {'SESSDATA': '1502a8ee%2C1571610493%2C60b13f91', 'csrf':'5524c8c121497774904472148b122504', 'roomid':'686555', 'msg': '>??<'}
# headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
# r = requests.post(url, data=json.dumps(data), headers=headers)