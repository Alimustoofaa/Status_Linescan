import os
import uvicorn
import subprocess
from fastapi import FastAPI, HTTPException

app = FastAPI(docs_url=None, redoc_url=None)

def get_ip_target():
    try:
        ipv4_eth0 = os.popen('ip addr show eth0').read().split("inet ")[1].split("/")[0]
        last_eth0 = ipv4_eth0.split('.')[-1]
        target_ip = f'192.168.100.{last_eth0}'
    except:
        target_ip, ipv4_eth0 = '', ''
    return target_ip, ipv4_eth0

target_ip, host_ip = get_ip_target()
    
@app.get('/')
def read_root():
    return {
        'status': True,
        'message': 'service status linescan'
    }
    
@app.get('/linescan')    
def status_linescan():
    try:
        command = ['ping', '-c', '1', target_ip]
        output = subprocess.run(command, capture_output=True, text=True)
        if output.returncode == 0:
            status = 'OK'
            message = 'Linescane Connected'
        else:
            status = 'NOT OK'
            message = 'Linescane Disconnected'
        return {
            'status': status,
            'ip_target': target_ip,
            'message': message
        }
    except: HTTPException(status_code=400, detail='Failed ping ip')
    
if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=9001,
        reload=True,
        workers=1,
    )