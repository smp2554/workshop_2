import json
import re, os
import pymysql
import requests
import random
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import date, timedelta
from flask import Flask, render_template, request, session, redirect, abort
from selenium import webdriver

app = Flask(__name__, template_folder="template", static_folder="static")  
app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.secret_key="twomin"
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 5

db = pymysql.connect(
    user='root',
    passwd='931022',
    host='localhost',
    db='web',
    charset='utf8',
    cursorclass=pymysql.cursors.DictCursor
)



def get_menu():
    cursor = db.cursor()
    cursor.execute("select id, title from topic")
    menu = [f"<li><a href='/{row['id']}'>{row['title']}</a></li>"
            for row in cursor.fetchall()]
    return '\n'.join(menu)

def get_review():
    menu_temp1 = "<li><a href='/reviews/{0}'>{0}</a></li>"
    menu=[e for e in os.listdir('Review') if e[0] != '.']
    return "\n".join([menu_temp1.format(m) for m in menu])

# def get_template(filename):
#     print(filename)
#     with open( filename, 'r', encoding='utf-8')as f:
#         template=f.read()
#     return template    


# def get_wusinsa_image():
#     driver = webdriver.Chrome('/workshop_second/chromedriver')


    

# 첫 페이지
@app.route("/")

def index():
    name = session['user']['name'] if 'user' in session else ''
    return render_template('main.html',
                           username=name,
                           id="",
                           menu=get_menu())



# main2 page 접속

@app.route('/main2')
def main2():
    if 'user' in session:
        title = '★ Welcome!! ' + session['user']['name']
    else:
        title = 'Welcome'
        
    
    return render_template('main2.html',
                           title=title,
                           id="",
                           menu=get_menu())


## 로그아웃
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# NEW OR OLD
@app.route('/<title>')
def html(title):
   
    
     return render_template(f'{title}.html',
                            title=title,
                            menu=get_menu())



# @app.route("/reviews/<title>")
# def reviews(title):
#     menu=get_review()
#     with open(f'Review/{title}', 'r', encoding="utf-8") as f:
#         content = f.read()
# #     cursor = db.cursor()
# #     cursor.execute(f"select * from topic where id = '{id}'")
# #     topic = cursor.fetchone()

# #     if topic is None:
# #         abort(404)
    
# #    # return render_template('template.html', id=topic['id'], title=topic['title'], content=topic['description'], menu=get_menu()) 
#     return render_template('review.html', 
#                             content=content, 
#                             menu=menu)



@app.route("/delete/<id>")
def delete(id):
    cursor = db.cursor()
    cursor.execute(f"delete from review where id = '{id}'")
    db.commit()
    
    return redirect("/review")



@app.route("/review", methods=['GET', 'POST'])
def review():
   
    if request.method=="GET":
        
        cursor = db.cursor()
        sql = "SELECT *  FROM `review`"
        cursor.execute(sql)
        #reviews = [f"<li><a href='/{row['id']}'> {row['title']}</a></li>" for row in cursor.fetchall()]
        
        reviews = cursor.fetchall()
        #print(reviews)
        return render_template('review.html', 
                               message='', 
                               menu=reviews,
                               name='')
    
#     menu = [f"<li><a href='/{row['id']}'> {row['title']}</a></li>" for row in cursor.fetchall()]
#     return '\n'.join(menu)    
    
    
    
    elif request.method=="POST":
 
        cursor = db.cursor()
        sql = f"""
            insert into review (title, description)
            values ('{request.form['title']}', '{request.form['desc']}')
        """
        cursor.execute(sql)
        db.commit() #pymysql 문법

        return redirect('/review')
    
    
    
    

#로그인
@app.route("/login_page", methods=['GET', 'POST'])
def login():
    message = ""
    if request.method == 'POST':
        cursor = db.cursor()
        cursor.execute(f"""
            select id, name, profile, password from author 
            where name = '{request.form['id']}'""")
        user = cursor.fetchone()
        
        if user is None:
            message = "회원이 아닙니다."
        else:
            cursor.execute(f"""
            select id, name, profile, password from author 
            where name = '{request.form['id']}' and 
                  password = SHA2('{request.form['pw']}', 256)""")
            user = cursor.fetchone()
            
            if user is None:
                message = "패스워드를 확인해 주세요"
            else:
                # 로그인 성공에는 메인으로
                session['user'] = user
                return redirect("/main2")
    
    return render_template('login_page.html', 
                           message=message)




 #쇼핑몰 별 실시간 순위 PAGE(우신사, 무신사, W컨셉, 29cm)
@app.route('/shop_ranking')
def get_ranking(): 

    return render_template('shop_ranking.html') 
    
    

#우신사 실시간 순위 
@app.route('/shop_ranking/wusinsa', methods=['GET', 'POST'])
def get_ranking_wusinsa():
    time=datetime.now()
    
    if request.method=="GET":
    
        res = requests.get("https://wusinsa.musinsa.com/app/contents/bestranking?u_cat_cd=")
        soup= BeautifulSoup(res.content, 'html.parser')
        product_rank=[]

        for tag in soup.select(".article_info"):
            brand = tag.select(".item_title > a")[0].get_text()
            name = tag.select(".list_info > a")[0].get_text().strip()
            price = tag.select(".price")[0].get_text()
            if len(tag.select(".txt_cnt_like")) > 0:
                like_num= tag.select(".txt_cnt_like")[0].get_text().strip()
            else:
                like_num=0
            regex = re.compile("(\d+,\d+원)")
            real_price = re.findall(regex, price)
            if len(real_price) == 2:
                sale_price=real_price[1]
            else: 
                sale_price=real_price[0]
            product_rank.append({'브랜드명': brand,
                     '이름': name,
                     '가격': sale_price,
                     '좋아요': like_num})
    
        return render_template('shoppingmall.html', 
                           title = "우신사", 
                           action='get_ranking_wusinsa',
                           products=product_rank,
                           time = time.strftime('%Y-%m-%d %H:%M:%S')  )
            
    
    elif request.method=="POST":
        
        price1 = request.form['price1']
        price2 = request.form['price2']            
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.implicitly_wait(3)
        url = "https://wusinsa.musinsa.com/app/contents/bestranking?u_cat_cd="
        driver.get(url)


        driver.find_element_by_css_selector('.division_search_input').clear()
        driver.find_element_by_name('price1').send_keys("price1")
        driver.find_element_by_name('price2').send_keys("price2")
        # time.sleep(1)
        driver.find_element_by_css_selector('#catelist > div.division_box.hover_box.box_division_price.box_division_group > dl > dd > ul > li.division_search_box.search_price > span.division_search_btn').click()

        url_2=f"https://wusinsa.musinsa.com/app/contents/bestranking/?d_cat_cd=&u_cat_cd=&range=nw&price={price1}%5E{price2}"

        res = requests.get(url_2)
        soup= BeautifulSoup(res.content, 'html.parser')
        product_rank=[]


        for tag in soup.select(".article_info"):
                brand = tag.select(".item_title > a")[0].get_text()
                name = tag.select(".list_info > a")[0].get_text().strip()
                price = tag.select(".price")[0].get_text()
                if len(tag.select(".txt_cnt_like")) > 0:
                    like_num= tag.select(".txt_cnt_like")[0].get_text().strip()
                else:
                    like_num=0
                regex = re.compile("(\d+,\d+원)")
                real_price = re.findall(regex, price)
                if len(real_price) == 2:
                    sale_price=real_price[1]
                else: 
                    sale_price=real_price[0]
                product_rank.append({'브랜드명': brand,
                         '이름': name,
                         '가격': sale_price,
                         '좋아요 수': like_num})


        return render_template('shoppingmall.html', 
                           title = "우신사", 
                           action='get_ranking_wusinsa',
                           products=product_rank,
                          time = time.strftime('%Y-%m-%d %H:%M:%S'))
    
    
    
#무신사 실시간 순위       
@app.route('/shop_ranking/musinsa', methods=['GET', 'POST'])
def get_ranking_musinsa():
    time=datetime.now()
    
    if request.method=="GET":
    
        res = requests.get("https://store.musinsa.com/app/contents/bestranking")
        soup= BeautifulSoup(res.content, 'html.parser')
        product_rank=[]

        for tag in soup.select(".article_info"):
            brand = tag.select(".item_title > a")[0].get_text()
            name = tag.select(".list_info > a")[0].get_text().strip()
            price = tag.select(".price")[0].get_text()
            if len(tag.select(".txt_cnt_like")) > 0:
                like_num= tag.select(".txt_cnt_like")[0].get_text().strip()
            else:
                like_num=0
            regex = re.compile("(\d+,\d+원)")
            real_price = re.findall(regex, price)
            if len(real_price) == 2:
                    sale_price=real_price[1]
            else: 
                    sale_price=real_price[0]
            product_rank.append({'브랜드명': brand,
                         '이름': name,
                         '가격': sale_price,
                         '좋아요': like_num})
    
        return render_template('shoppingmall.html', 
                           title = "무신사", 
                           action='get_ranking_musinsa',
                           products=product_rank,
                            time = time.strftime('%Y-%m-%d %H:%M:%S'))
            
    
    elif request.method=="POST":
        
        price1 = request.form['price1']
        price2 = request.form['price2']            
        
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver', options=options)
        driver.implicitly_wait(3)
        url = "https://store.musinsa.com/app/contents/bestranking"
        driver.get(url)


        driver.find_element_by_css_selector('.division_search_input').clear()
        driver.find_element_by_name('price1').send_keys("price1")
        driver.find_element_by_name('price2').send_keys("price2")
        # time.sleep(1)
        driver.find_element_by_css_selector('#catelist > div.division_box.hover_box.box_division_price.box_division_group > dl > dd > ul > li.division_search_box.search_price > span.division_search_btn').click()

        url_2=f"https://store.musinsa.com/app/contents/bestranking/?d_cat_cd=&u_cat_cd=&range=nw&price={price1}%5E{price2}"
        res = requests.get(url_2)
        soup= BeautifulSoup(res.content, 'html.parser')
        product_rank=[]


        for tag in soup.select(".article_info"):
                brand = tag.select(".item_title > a")[0].get_text()
                name = tag.select(".list_info > a")[0].get_text().strip()
                price = tag.select(".price")[0].get_text()
                if len(tag.select(".txt_cnt_like")) > 0:
                    like_num= tag.select(".txt_cnt_like")[0].get_text().strip()
                else:
                    like_num=0
                regex = re.compile("(\d+,\d+원)")
                real_price = re.findall(regex, price)
                if len(real_price) == 2:
                    sale_price=real_price[1]
                else: 
                    sale_price=real_price[0]
                product_rank.append({'브랜드명': brand,
                         '이름': name,
                         '가격': sale_price,
                         '좋아요 수': like_num})


        return render_template('shoppingmall.html', 
                           title = "무신사", 
                           action='get_ranking_musinsa',
                           products=product_rank,
                            time = time.strftime('%Y-%m-%d %H:%M:%S'))
    
    

    
@app.route("/favicon.ico")
def favicon():
    return abort(404)    
    
app.run(port = 8010) #파이썬파일 실행 가능 (포트번호 지정)



# @app.route("/dbtest")
# def dbtest():
#     cursor = db.cursor()
#     cursor.execute("select * from topic")
#     return str(cursor.fetchall())



#encoding="utf-8"


        
        
        
        
        
        
        
        
        
# #우신사 실시간 순위 
# @app.route('/shop_ranking/wusinsa')
# def get_ranking_wusinsa():

#     res = requests.get("https://wusinsa.musinsa.com/app/contents/bestranking?u_cat_cd=")
#     soup= BeautifulSoup(res.content, 'html.parser')
#     product_rank=[]

#     for num in soup.select("list-box.box"):
#         rank_num = tag.select(".n-label")[0].get_text()
    
#     for tag in soup.select(".article_info"):
#         brand = tag.select(".item_title > a")[0].get_text()
#         name = tag.select(".list_info > a")[0].get_text().strip()
#         price = tag.select(".price")[0].get_text()
#         if len(tag.select(".txt_cnt_like")) > 0:
#             like_num= tag.select(".txt_cnt_like")[0].get_text().strip()
#         else:
#             like_num=0
#         regex = re.compile("(\d+,\d+원)")
#         real_price = re.findall(regex, price)[0]
#         product_rank.append({'브랜드명': brand,
#                  '이름': name,
#                  '가격': real_price,
#                  '좋아요 수': like_num})

#         #print(price.replace('\t', '').strip())
# #     print("*" * 30)   
# #     print("실시간 랭킹 순위 ")
# #     print("*" * 30)   

# #     for i, rank in enumerate(product_rank):
# #         print(i+1,"위", rank)
        
    
#     return render_template('shoppingmall.html', 
#                            title = "우신사", 
#                            action='get_ranking_wusinsa',
#                            products=product_rank)
        

    
    

# @app.route("/<title>")
# def content(title):
#     cursor = db.cursor()
#     cursor.execute(f"select * from page where title = '{title}'")
#     topic = cursor.fetchone()
    
#     if topic is None:#토픽이 없으면
#         abort(404)
        
    
#     return render_template('main2.html', #토픽이 있으면
#                            id = topic ['id'],
#                            title=topic['title'],
#                             content=topic['description'],
#                            menu=get_menu())
