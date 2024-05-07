from fastapi import FastAPI, Request, Form, Query, Request, Response, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from dao.todoDAO import selectAll, register, selectOne, modify, delete
from dao.memberDAO import getWithPassword
from dto.todoDTO import TodoDTO
from dto.memberDTO import MemberDTO
from datetime import date, datetime
from starlette.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware


app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/todo/list")
async def read_todos(request: Request):
    todos = selectAll()
    loginInfo = request.session.get('loginInfo')   
    return templates.TemplateResponse("list.html", {"request": request, "todos": todos, "loginInfo" : loginInfo})


@app.get("/todo/register")
async def register_todos(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/todo/register")
async def create_todo(title: str = Form(...), 
                    dueDate: date = Form(...), 
                    finished: bool = Form(False)): # 여기서 기본값을 False로 설정
    # 여기에서 TodoDTO를 사용하여 인스턴스 생성
    todoDTO = TodoDTO(title=title, dueDate=dueDate, finished=finished)
    # DB에 todo 등록
    register(todoDTO)    
    # 데이터가 처리되었다고 가정하고, 처리된 데이터를 반환하거나 리다이렉션 수행
    return RedirectResponse(url="/todo/list", status_code=303)

@app.get("/todo/read")
async def read_todo(request: Request, tno: int = Query(..., description="The ID of the todo to fetch")):
    todo = selectOne(tno)
    if todo:
            # Pydantic 모델 인스턴스 생성
            todoDTO = TodoDTO(
                tno=todo['tno'],
                title=todo['title'],
                dueDate=todo['duedate'],  # 데이터베이스에서 날짜 형식 확인 필요
                finished=todo['finished']
            )    
    return templates.TemplateResponse("read.html", {"request": request, "todoDTO" : todoDTO})

@app.get("/todo/modify")
async def modify_todo_view(request: Request, tno: int =Query(..., description="The ID of the todo to fetch")):
    todo = selectOne(tno)
    if todo:
            todoDTO = TodoDTO(
                tno=todo['tno'],
                title=todo['title'],
                dueDate=todo['duedate'],  # 데이터베이스에서 날짜 형식 확인 필요
                finished=todo['finished']
            )
    return templates.TemplateResponse("modify.html", {"request": request, "todoDTO" : todoDTO}) 

@app.post("/todo/modify")
async def modify_todo(tno : int = Form(...),
                    title : str = Form(...),
                    dueDate : date = Form(...),
                    finished : bool = Form(False)):
    todoDTO = TodoDTO(tno = tno, title = title, dueDate = dueDate, finished = finished)
    modify(todoDTO)
    return RedirectResponse(url="/todo/list", status_code=303)

@app.post("/todo/delete")
async def delete_todo(tno : int = Form(...)):
    delete(tno)
    return RedirectResponse(url='/todo/list', status_code=303)

@app.get("/logIn")
async def login_member_view(request : Request):
    return templates.TemplateResponse("login.html", {"request" : request})

# 세션 미들웨어 설정
app.add_middleware(SessionMiddleware, secret_key="!secret!")

# 로그인 기능
@app.post("/logIn")
async def login_member(request: Request, mid: str = Form(...), mpw: str = Form(...)):
    memberDTO = MemberDTO(mid=mid, mpw=mpw)
    memberDTO_n = getWithPassword(memberDTO)
    if memberDTO_n:
        request.session['loginInfo'] = dict(memberDTO_n)
        return RedirectResponse(url="/todo/list", status_code=303)
    return "Login Failed"

# 로그아웃 기능
@app.post("/logOut")
async def logout_member(request: Request):
    request.session.pop('loginInfo', None)
    return RedirectResponse(url='/todo/list', status_code=303)
