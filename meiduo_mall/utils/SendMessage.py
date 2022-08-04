from libs.ronglian_sms_sdk import SmsSDK

accId = '8aaf0708825efdb2018269691a4303af'
accToken = 'fde70b9c5ef84184a2783e2b3cf6ccdd'
# 容联云通讯分配的应用ID
appId = '8aaf0708825efdb2018269691b3303b6'

def send_message(tid,mobile,datas):
    sdk = SmsSDK(accId, accToken, appId)
    # tid = '容联云通讯创建的模板'
    # mobile = '手机号1,手机号2'
    # datas = ('变量1', '变量2')
    resp = sdk.sendMessage(tid, mobile, datas)
    return resp


