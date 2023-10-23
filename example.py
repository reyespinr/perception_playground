@app.get("/bootstrap_admin", response_class=HTMLResponse)
async def bootstrap_admin_page(request: Request):
    return templates.TemplateResponse("bootstrap_admin.html", {"request": request})


@app.post("/bootstrap_admin")
def bootstrap_admin(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    # Check if any user exists
    existing_users = db.query(User).all()
    if existing_users:
        raise HTTPException(
            status_code=403, detail="Admin user already exists!")

    hashed_password = get_password_hash(password)
    admin_user = User(
        username=username, hashed_password=hashed_password, role=UserRole.ADMIN.value)

    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return {"id": admin_user.id, "username": admin_user.username, "role": admin_user.role}
