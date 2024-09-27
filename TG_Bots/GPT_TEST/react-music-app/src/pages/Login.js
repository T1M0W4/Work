import React from 'react';

const Login = () => {
  return (
    <div>
      <h1>Страница Входа</h1>
      <form>
        <div>
          <label htmlFor="username">Имя пользователя:</label>
          <input type="text" id="username" name="username" required />
        </div>
        <div>
          <label htmlFor="password">Пароль:</label>
          <input type="password" id="password" name="password" required />
        </div>
        <button type="submit">Войти</button>
      </form>
    </div>
  );
};

export default Login;