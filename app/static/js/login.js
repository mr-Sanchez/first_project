function checkForm() {
    loginField = document.querySelector('#exampleInputEmail1');
    passwordField = document.querySelector('#exampleInputPassword1');
    submitButton = document.querySelector('#sbm');
    if (loginField.value === '' || passwordField.value === '') {
        let notification = document.querySelector('.login-ntf');
        if (!notification) {
            notification = document.createElement('span');
            notification.className = 'login-ntf';
            notification.setAttribute("style", "color: brown; display: block; margin-bottom: 10px;");
            notification.textContent = 'Все поля должны быть заполнены';
        }  
        submitButton.before(notification);
        return false;
    }
    return true;
}
