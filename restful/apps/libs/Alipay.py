import json
from apps.utils.alipay import AliPay, ISVAliPay


class OrderAlipay(object):
    def __init__(self,current_app):
        self.alipay_url_prefix = 'https://openapi.alipaydev.com/gateway.do?'
        a = current_app.config['ALIPAY_PUBLIC_KEY']
        self.alipay = AliPay(
            appid = current_app.config['APP_ID'],
            app_notify_url = None,
            alipay_public_key_string = current_app.config['ALIPAY_PUBLIC_KEY'],
            app_private_key_string = current_app.config['ALIPAY_PRIVATE_KEY'],
            sign_type = "RSA2",
            debug = True
        )

    def web_pay(self):
        pass

    def mobile_pay(self):
        pass

    def app_pay(self):
        pass

    def refund(self,refund_amount,out_trade_no,trade_no):
        result = self.alipay.api_alipay_trade_refund(refund_amount,out_trade_no=out_trade_no,trade_no = trade_no)
        if result["code"] == "10000":
            return True
        else:
            return False


    def get_pay_url(self,type,out_trade_no,total_amount,subject,return_url,notify_url = None):
        # 手机/PC网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        # 判断支付类型
        pay_function = self._get_pay_type(type)
        order_string = pay_function(
            out_trade_no = out_trade_no,  # 订单编号 不重复
            total_amount = total_amount,  # 支付金额  0.01小数两位
            subject = subject,  # 订单标题
            return_url = return_url,  # 返回链接地址 http://127.0.0.1:5000/order.html
            notify_url = notify_url  # 可选, 不填则使用默认notify url
        )

        # 构建跳转到的支付地址
        pay_url = self.alipay_url_prefix + order_string
        return json.dumps({'code':'200','pay_url':pay_url})

    def verify(self,data):
        # data = request.form.to_dict()
        # sign 不能参与签名验证
        signature = data.pop("sign")
        # verify
        success = self.alipay.verify(data, signature)
        if success and data["trade_status"] in ("TRADE_SUCCESS", "TRADE_FINISHED"):
            print("trade succeed")

    def paid(self,out_trade_no):
        # 向alipay发起查询
        result = self.alipay.api_alipay_trade_query(out_trade_no=out_trade_no)
        # 这里的out_trade_no可以用GET到的
        if result.get("trade_status", "") == "TRADE_SUCCESS":
            return result.get('trade_no')  # 这里使用支付宝返回的订单号来显示支付成功
        return 'fail'

    def _get_pay_type(self,type):
        """
        判断支付方式
        """
        pay_type = None
        if type == 'wap':
            pay_type = getattr(self.alipay,'api_alipay_trade_wap_pay')
        elif type == 'pc':
            pay_type = getattr(self.alipay, 'api_alipay_trade_page_pay')
        elif type == 'app':
            pay_type = getattr(self.alipay, 'api_alipay_trade_app_pay')

        return pay_type

