import json
import re
import logging
from django import http
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from sqlalchemy import desc
from sqlalchemy.orm import session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import exc

from ranking_list.util.response_code import RETCODE
from .models import user_ranking

logger=logging.getLogger('django')
engine = create_engine('mysql+pymysql://root:mysql@127.0.0.1:3306/ranking_list?charset=utf8', echo=False)
session_maker = sessionmaker(bind=engine)
session = scoped_session(session_maker)

"""获取排行榜数据"""
class ranks(View):
    def get(self,request,pk):
        min=request.GET.get('min')
        max = request.GET.get('max')
        try:
            try:
                #参数校验 ,符合条件查询指定范围,不符合条件查询全部
                min=int(min)
                max=int(max)
                if (not min<=max) or (min<1) or (max<1):
                    raise Exception
            except Exception as e:
                #查询全部排行
                cursor = session.execute(
                    'select t.score,t.client_code,(select count(s.score)+1 from user_ranking s where s.score>t.score) rank from user_ranking t order by t.score desc;',
                    )
            else:
                #查询指定范围排行
                cursor = session.execute(
                    'select t.score,t.client_code,(select count(s.score)+1 from user_ranking s where s.score>t.score) rank from user_ranking t order by t.score desc limit :min,:max;',
                    params={"min": min - 1, 'max': (max - min) + 1})

            #排行列表
            rank_list=[]

            ranks = cursor.fetchall()

            #把查询出来的排行拼接成字典
            for rank in ranks:
                rank_list.append({
                        'score': rank[0],
                        'cid': rank[1],
                         'no': rank[2],
                    })


            #查询当前客户端排行,并添加到字典
            cursor = session.execute('select t.score,t.client_code,(select count(s.score)+1 from user_ranking s where s.score>t.score) rank from user_ranking t where t.client_code=1;')
            result = cursor.fetchall()
            rank_list.append({'score':result[0][0],'cid':result[0][1],'no': result[0][2]})
        except exc.DatabaseError as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库操失败'})

        return http.JsonResponse({'code': RETCODE.OK, 'errmsg': 'OK', 'rank_list': rank_list})



'''获取页面,上传客户端号和分数'''
class rank(View):

    def get(self,request):
        return render(request,'list.html')


    def post(self,request):
        dict=json.loads(request.body.decode())
        cid=dict.get('cid')
        score=dict.get('score')

        #参数校验
        if not all([re.match(r'^\d+$',cid),re.match(r'[1-9]\d{0,6}$|10000000',score)]):
            return http.HttpResponseForbidden("客户端编号和分数为数字,分数范围为1...10000000")

        score=int(score)

        #查询当前客户端有没有该用户

        try:
            rank=session.query(user_ranking).filter(user_ranking.client_code == cid).first()

            #没有就创建,有就修改
            if not rank:
                rank=user_ranking( client_code = cid,score = score)
                session.add(rank)
                session.commit()
            else:
                rank.score=score
                session.commit()

        except exc.DatabaseError as e:
            logger.error(e)
            return http.JsonResponse({'code': RETCODE.DBERR, 'errmsg': '数据库操失败'})

        return JsonResponse({'code':RETCODE.OK,'errmsg':'ok'})


