from django.shortcuts import render, redirect

from django.conf import settings
import requests

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import JSONParser


class KhaltiVerifyPayment(APIView):

    # parser_classes = [JSONParser]

    def post(self, request):
        token = request.POST.get('token')
        amount = request.POST.get('amount')

        url = settings.KHALTI_VERIFY_URL
        auth_key = "Key {}".format(settings.KHALTI_SECRET_KEY)
        payload = {
        "token": token,
        "amount": amount,
        }
        headers = {
        "Authorization": auth_key
        }
        try:
            response = requests.post(url, payload, headers = headers)
            if response.status_code == 200 :
                return Response({
                    'status':"Success",
                    'details':response.json(),
                }, status=response.status_code)

            else:
                return Response({
                    'status':response.status_code,
                    'details':response.json(),
                }, status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({
                "status": "Request error occurred",
                "details": response.json(),
            })


def esewa(request):
    return render(request, "payment/eSewa.html")


class EsewaVerifyView(APIView):

    def get(self, request, *args, **kwargs):
        import xml.etree.ElementTree as ET
        oid = request.GET.get("oid")
        amt = request.GET.get("amt")
        refId = request.GET.get("refId")
        print("------"+refId+"-----")

        url = "https://uat.esewa.com.np/epay/transrec"
        d = {
            'amt': amt,
            'scd': 'EPAYTEST',
            'rid': refId,
            'pid': oid,
        }

        response = requests.post(url, d)
        root = ET.fromstring(response.content)
        status = root[0].text.strip()
        print(response.text)
        if status == "Success":
            return redirect("payment:success")
        else:
            return redirect("payment:fail")



def fail(request):
    return render(request, "payment/fail.html")

def success(request):
    return render(request, "payment/success.html")

def home(request):
    return render(request, "payment/index.html")