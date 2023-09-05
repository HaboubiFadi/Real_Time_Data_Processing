from django.shortcuts import render,HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

import sys 
sys.path.append('Django/Api_setting/Api/')
from Service import verifier_request,Create_json,produce_request,Consume_data,initiat_producer,Initiat_Consumer
# Create your views here.





kafka_server_confi={'bootstrap.servers':"broker:9092",'group.id':'api_consumer','enable.auto.commit': True,
        'auto.offset.reset': 'earliest'}



reception_api='reception_api'
emission_api='emission_api'








def home(request):
    return HttpResponse("hello world")

@csrf_exempt
def json_reqest(request):
    if request.method == 'GET':
        #data=json.load(request.body)
        bool=verifier_request(request)
        print('verifier request statue:',bool[0])
        
        if bool[0] ==True:
            json_object=Create_json(request)    
            print('ssssss',emission_api)
            producer=initiat_producer({'bootstrap.servers':"broker:9092"})
            consumer=Initiat_Consumer(kafka_server_confi)
            consumer.subscribe([reception_api])
            key=produce_request(producer,json_object,emission_api)
            value=Consume_data(consumer,key)
            response_data={'message':'Data received succefully','value':value,'description':bool[1]}
            return JsonResponse(response_data, status=200)
        else:
            response_data={'message':'Error : invalid syntaxe','description':bool[1]}


            return JsonResponse(response_data, status=405)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)    