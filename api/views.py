from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from api import models
from rest_framework import serializers

'''


class MyCharField(serializers.CharField):
    "自定义模板中需要序列化字段的类，目的是自定制多对多关系中的返回值"
    def to_representation(self, value):
        # value代表，当前user对象关联的觉得对象
        role_list = []
        for each in value:
            role_list.append(each.name)
        return role_list

# 建立一个继承自serializers.Serializers的类，这种需要自己定义需要序列化的字段
class UserSerializer(serializers.Serializer):
    "相当于建立一个序列化的模板，来规定需要的字段"
    # 单表中的字段
    id = serializers.CharField()  # obj.id (要是没有写source=xxx,就会执行obj.id)
    name = serializers.CharField()
    pwd =serializers.CharField()
    #跨表查询(多对一)
    group = serializers.CharField(source='group.title')  # source拿到当前对象的group属性的，
    menu_ttile = serializers.CharField(source='group.mu.name')
    menu_id = serializers.CharField(source='group.mu.id')    # 字符串内部做判断，可执行，则会执行

    # 多对多(自定制当前字段序列化之后返回中的内容)
    # role_list = serializers.CharField(source='roles.all')
    # 这种，在最后显示的时候，只能做成这样子 "role_list": "<QuerySet [<Role: Role object>, <Role: Role object>]>"

    # 方法1：定制to_representation方法
    # 针对上种情况，定制返回值，继承自(serializers.CharField)
    # role_list = MyCharField(source='roles.all')

    # 方法2:(其实返回的内容，还是需要自定义MyCharField()类定制返回的值，只是value指定每个role对象，)
    # role_list = serializers.ListField(child=serializers.CharField(),source='roles.all')

    # 方法3：(也需要自定制get_字段名,定义此子字段返回值，定制性更好，=====推荐使用====)
    role_list = serializers.SerializerMethodField()

    def get_role_list(self,obj):# obj就是当前user对象
        li = []
        roles_list = obj.roles.filter(id=1)
        roles_list = obj.roles.all()
        for i in roles_list:
            li.append({'id':i.id,'name':i.name})
        return li



class UserView(APIView):

    # 单表
    # def get(self,request,*args,**kwargs):
    #     user_list = models.UserInfo.objects.all()
    #     ser = UserSerializer(instance=user_list,many=True)
    #     print(ser.data)
    #     return Response(ser.data)

    # 跨表查询
    def get(self,request,*args,**kwargs):
        user_list = models.UserInfo.objects.all()
        ser = UserSerializer(instance=user_list,many=True)
        print(ser.data)
        return Response(ser.data)
'''


#######################################################################
# 自己不用写字段的方式：继承的类不一样

class UserSerializer(serializers.ModelSerializer):
    x1 = serializers.CharField(source='name')  # 自定义字段，必须定义source
    class Meta:
        model = models.UserInfo
        # fields = '__all__'
        fields = ['name','pwd','group','x1']
        depth = 3


class UserView(APIView):
    def get(self,request,*args,**kwargs):
        user_list = models.UserInfo.objects.all()
        ser = UserSerializer(instance=user_list,many=True)
        print(ser.data)
        return Response(ser.data)


















