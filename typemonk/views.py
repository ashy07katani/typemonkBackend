from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import serializers
from oauth2_provider.decorators import protected_resource
from oauth2_provider.views.base import TokenView
from django.utils.decorators import method_decorator
from oauth2_provider.models import get_access_token_model
from oauth2_provider.signals import app_authorized
from django.views.decorators.debug import sensitive_post_parameters
from oauth2_provider.models import AccessToken
from django.http import HttpResponse
import requests
import base64
import json
# from django.contrib.auth.decorators import login_required
# Create your views here.
from . import models

class CustomTokenView(TokenView):
   # @api_view(["POST"])
    @method_decorator(sensitive_post_parameters("password"))
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        body = json.loads(response.content)
        access_token = body.get("access_token")
        token = get_access_token_model().objects.get(token=access_token)
        body["member"] = {
            "id": token.user.id,
            "email": token.user.email,
            "username": token.user.username,
        }
        response.content = json.dumps(body)
        return response    

        


@api_view(['GET'])
def getTests (request):
    test = {
        'id':1,
        'user':"ashish",
        'time':120,
        'wpm':91,
        'accuracy':100,
        'raw':91,
        'dateTaken':"22 oct 2023"
    }
    return Response(test)

@protected_resource()
@api_view(['GET'])
def getUserTests (request):
    print("currently logged in user is ",request.user.username)
    userid = models.UserProfile.objects.get(userName=request.user.username)
    print("values that I got from the model",userid.id)
    testListQuerySet = models.TypingTest.objects.filter(user=userid).order_by('-wpm','-time')
    serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
    return Response(serializer.data)
    

@api_view(['GET'])
def getAllTests (request):

    testListQuerySet = models.TypingTest.objects.all().order_by('-time','-wpm',)
    serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getSpecificTimeAllTests(request):
        time=request.query_params.get('time')
        testListQuerySet = models.TypingTest.objects.filter(time=time).order_by('-wpm')
        serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
        return Response(serializer.data)


@protected_resource()
@api_view(['GET'])
def getUserSpecificTimeTests (request):
    time=request.query_params.get('time')
    userid = models.UserProfile.objects.get(userName=request.user.username)
    testListQuerySet = models.TypingTest.objects.filter(user=userid,time=time).order_by('-wpm')
    serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
    return Response(serializer.data)

@protected_resource()
@api_view(['GET'])
def getAllUser (request):
    UserListQuerySet = models.UserProfile.objects.all()
    serializer = serializers.UserSerializer(UserListQuerySet,many=True)
    return Response(serializer.data)

@api_view(["POST"])
def getOauth (request):
    resopnsePayload={}
    if request.method == 'POST':
        clientId = '91aTbwBlowKhqlGk2GwJV597q0KjYlNgz9l3PMSC'
        clientSecret = 'sUkl8S4kX8dQg8CehBjZPeKLCRwUWPfsjrEOVt1sE3gAwdXyjP4jrmGk909DYsB6cSnFzj6DosvIecgxVaun8RNs1GpExCSQvUnJwfUnWmuGqk8CyzhyensGFtDGoqyp'
        authorizationHeaderValue = "Basic " + str(base64.b64encode(bytes(clientId+":"+clientSecret,'utf-8')))[1:]
        url = "http://localhost:8000/o/token/"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization":authorizationHeaderValue
            }
        payload = {   
            "grant_type": 'password',
            "username":request.POST["username"],
            "password":request.POST["password"] 
        }
        result = requests.post(url,  data=payload, headers=header)
        resopnsePayload=result.json()
        if result.status_code == 200:
            resopnsePayload["username"] = request.POST["username"]
        return Response(resopnsePayload,status=result.status_code)

@api_view(["POST"])
def registerUser (request):
        resopnsePayload={}
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email")
        user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password)
        userInstance = models.UserProfile(user=user,userName=username,email=email)
        userInstance.save()
        clientId = '91aTbwBlowKhqlGk2GwJV597q0KjYlNgz9l3PMSC'
        clientSecret = 'sUkl8S4kX8dQg8CehBjZPeKLCRwUWPfsjrEOVt1sE3gAwdXyjP4jrmGk909DYsB6cSnFzj6DosvIecgxVaun8RNs1GpExCSQvUnJwfUnWmuGqk8CyzhyensGFtDGoqyp'
        authorizationHeaderValue = "Basic " + str(base64.b64encode(bytes(clientId+":"+clientSecret,'utf-8')))[1:]
        url = "http://localhost:8000/o/token/"
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization":authorizationHeaderValue
            }
        payload = {   
            "grant_type": 'password',
            "username":request.POST.get("username"),
            "password":request.POST.get("password") 
        }
        result = requests.post(url,  data=payload, headers=header)
        resopnsePayload=result.json()
        if result.status_code == 200:
            
            resopnsePayload["username"] = username
        return Response(resopnsePayload,status=result.status_code)


@api_view(["POST"])
def googleSignIn (request):
        resposnePayload = {}
        token = request.headers.get("token")      
        clientId = '91aTbwBlowKhqlGk2GwJV597q0KjYlNgz9l3PMSC'   
        clientSecret = 'sUkl8S4kX8dQg8CehBjZPeKLCRwUWPfsjrEOVt1sE3gAwdXyjP4jrmGk909DYsB6cSnFzj6DosvIecgxVaun8RNs1GpExCSQvUnJwfUnWmuGqk8CyzhyensGFtDGoqyp'
        url = 'http://localhost:8000/auth/convert-token'
        header = {
            "Content-Type": "application/x-www-form-urlencoded"
            }
        payload = {   
            "grant_type": 'convert_token',
            "client_id" : clientId,
            "client_secret" :clientSecret,
            "backend":"google-oauth2",
            "token":token
        }
        result = requests.post(url,data=payload,headers = header)
        resopnsePayload=result.json()
        resopnsePayload["username"] = AccessToken.objects.get(token=resopnsePayload["access_token"]).user.username
        return Response(resopnsePayload,status=result.status_code)

'''
{
"username":"shubham",
"password":"ashish.10",
"email":"shubham@email.com"
}

convert_token
'''
    
        
        

    
    
    
    


