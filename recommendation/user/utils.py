@users.route('/register', methods = ['GET','POST'])
def update():
    if current_user.is_authenticated:
        flash(f'You are already logged in ','info')
        return redirect(url_for('main.home'))
    
    form = RegistrationForm()
    arm_sub = Arm.query.filter_by(name = "Art").first()
    form.arms.choices = [(g.name, g.name) for g in Arm.query.order_by('name').all()]
    for sub in arm_sub.arm_subjects:
        
        subjectForm = SubjectForm()
        subjectForm.name = sub.name
        subject = {
            "name" : sub.name,
            "rating": None
        } 
        # form.subjects.append_entry(subject)
        form.subjects.append_entry(subjectForm)
        # form.subjects.entries.append(subjectForm)
     
    if form.validate_on_submit():
        role = Role(name = "User")
        user = User(
            username = form.username.data,
            password = form.password.data,
            email = form.email.data,
            age = form.age.data,
            role = role,
            arm = form.arms.data
        )    
        
        for i in form.subjects:
            print(i)

        db.session.add_all([role, user])
        db.session.commit()
        
        flash(f'Your account has been created! You are now able to loggin','success')
        return redirect(url_for('users.login'))
    
    return render_template('register.html', title = 'Update', form = form)




# @users.route('/register', defaults = {'arm':"Art"},methods = ['GET','POST'])
# @users.route('/users/update', methods = ['GET','POST'])
# @login_required
# def update():
#     form = UpdateForm()
#     form.username.data = current_user.username
#     form.email.data = current_user.email
#     form.email(disabled= "disabled")
#     form.username(disabled= "disabled")
    
#     arm_sub = Arm.query.filter_by(name = "Art").first()
#     form.arms.choices = [(g.name, g.name) for g in Arm.query.order_by('name').all()]
#     for sub in arm_sub.arm_subjects:
        
#         subjectForm = SubjectForm()
#         subjectForm.name = sub.name
#         subjectForm.rating = None
#         subject = {
#             "name" : sub.name,
#             "rating": None
#         } 
#         form.subjects.append_entry(subjectForm)
#         # form.subjects.entries.append(subjectForm)
        
#     if form.submit.data == True:
       
#         current_user.age = form.age.data
#         current_user.arms = form.arms.data
        
#         print(form.subjects.data)
#         db.session.commit()
#         print(current_user)
#         return redirect(url_for('users.question'))
#     return render_template('test.html', title = 'Update', form = form)