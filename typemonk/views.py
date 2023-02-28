from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from . import serializers
from oauth2_provider.decorators import protected_resource
import requests
import base64
import json
# from django.contrib.auth.decorators import login_required
# Create your views here.
from . import models
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
    #testListQuerySet = models.TypingTest.objects.all()
    serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
    return Response(serializer.data)
    

@api_view(['GET'])
def getAllTests (request):

    testListQuerySet = models.TypingTest.objects.all().order_by('-time','-wpm',)
    serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
    return Response(serializer.data)
  #working right now heere 
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
    print("currently logged in user is ",request.user.username)
    userid = models.UserProfile.objects.get(userName=request.user.username)
    print("values that I got from the model",userid.id)
    testListQuerySet = models.TypingTest.objects.filter(user=userid,time=time).order_by('-wpm')
    #testListQuerySet = models.TypingTest.objects.all()
    serializer = serializers.TypingTestSerializer(testListQuerySet, many=True)
    return Response(serializer.data)
 #working right now heere  ends 
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
        # print('request parameter are : ',request.POST)
        # res = requests.post('http://localhost:8000/o/token', params=request.POST)
        # print(res)
        clientId = '91aTbwBlowKhqlGk2GwJV597q0KjYlNgz9l3PMSC'
        clientSecret = 'sUkl8S4kX8dQg8CehBjZPeKLCRwUWPfsjrEOVt1sE3gAwdXyjP4jrmGk909DYsB6cSnFzj6DosvIecgxVaun8RNs1GpExCSQvUnJwfUnWmuGqk8CyzhyensGFtDGoqyp'
        print("username",request.POST["username"],"password",request.POST["password"])
        authorizationHeaderValue = "Basic " + str(base64.b64encode(bytes(clientId+":"+clientSecret,'utf-8')))[1:]
        print("authorization header",authorizationHeaderValue)
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
            print(request.user)
            resopnsePayload["username"] = request.POST["username"]

        return Response(resopnsePayload,status=result.status_code)

@api_view(["POST"])
def registerUser (request):
        resopnsePayload={}
        username = request.POST.get("username")
        print("all is well1",username)
        password = request.POST.get("password")
        print("all is well2",password)
        email = request.POST.get("email")
        print("all is well3",email)
        user = User.objects.create_user(username=username,
                                     email=email,
                                     password=password)
        print("all is well4")
        userInstance = models.UserProfile(user=user,userName=username,email=email)
        print("all is well5")
        userInstance.save()
        print("all is well6")
        clientId = '91aTbwBlowKhqlGk2GwJV597q0KjYlNgz9l3PMSC'
        clientSecret = 'sUkl8S4kX8dQg8CehBjZPeKLCRwUWPfsjrEOVt1sE3gAwdXyjP4jrmGk909DYsB6cSnFzj6DosvIecgxVaun8RNs1GpExCSQvUnJwfUnWmuGqk8CyzhyensGFtDGoqyp'
        print("username",request.POST["username"],"password",request.POST["password"])
        authorizationHeaderValue = "Basic " + str(base64.b64encode(bytes(clientId+":"+clientSecret,'utf-8')))[1:]
        print("authorization header",authorizationHeaderValue)
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
        

'''
{
"username":"shubham",
"password":"ashish.10",
"email":"shubham@email.com"
}
'''
    
        
        

    
    
    
    


