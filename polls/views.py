from django.shortcuts import render
from rest_framework.response import Response
from .models import *
from polls.serializers import UserSerializer  # Import the serializer here
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from polls.helpers import send_otp_to_mobile
import uuid

class RegisterView(APIView) :
    
    def post(self, request)  :
            
        try :
            serializer = UserSerializer(data = request.data)
            print('serializer', serializer)
            if not serializer.is_valid() :
                return Response({'status' : 400, 'error': serializer.errors})
            
            serializer.save()
            
            data = request.data
            CurrentInst = User.objects.get(email = data.get('email')) 
            EmailVeriToken = uuid.uuid4()
        
            if CurrentInst and EmailVeriToken :
                CurrentInst.is_email_verified = True
                CurrentInst.email_verification_token = EmailVeriToken
                CurrentInst.save()
            return Response({'status': 200, 'message': 'an OTP sent on your number and email'})
            
        except Exception as e :
            print(e)
            return Response({'status': 400, 'error': 'Something Went to wrong'})
        
    def get(self, request) :
        student_objs = User.objects.all()
        serializer = UserSerializer(student_objs, many=True)
        print(request.user)
        return Response({'status': 200, 'payload':serializer.data, 'message': 'get all the data'})    
    
class VerifyOtp(APIView) :  
    
    def post(self, request) :
        try :
            data = request.data
            user_obj = User.objects.get(phone = data.get('phone')) # user_obj = User.objects.get(phone = data['phone']) 
            otp = data.get('otp')
            
            if user_obj.otp == otp :
                user_obj.is_phone_verified = True
                user_obj.save()
                return Response({'status' : 200, 'message': 'your OTP is verified'})
            return Response({'status': 403, 'message': 'your OTP is wrong'})
                         
        except Exception as e :
            print(e)        
            return Response({'status': 400, 'error': 'Something Went to wrong'})
 
    def patch(self, request):
        try:
            data = request.data
        
            # Use filter instead of get
            user_queryset = User.objects.filter(phone=data.get('phone'))
        
            if not user_queryset.exists():
                return Response({'status': 404, 'error': 'user not found!'})

            # Get the first user object from the queryset
            user_obj = user_queryset.first()    # ===== user_obj[0] =====

            status , time = send_otp_to_mobile(data.get('phone'), user_obj)
            
            if status : 
                return Response({'status': 200, 'message': 'New OTP sent successfully!'})
            return Response({'status': 429, 'error': f'Try again in {time} seconds.'})
    
        except Exception as e:
            print(e)
            return Response({'status': 400, 'error': 'Something went wrong. Please try again later.'})
        
        