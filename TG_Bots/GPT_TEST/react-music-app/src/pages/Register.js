import React from 'react';

const Register = () => {
  return (
    <div>
      <h1>Страница Регистрации</h1>
      <form>
        <div>
          <label htmlFor="username">Имя пользователя:</label>
          <input type="text" id="username" name="username" required />
        </div>
        <div>
          <label htmlFor="email">Электронная почта:</label>
          <input type="email" id="email" name="email" required />
        </div>
        <div>
          <label htmlFor="password">Пароль:</label>
          <input type="password" id="password" name="password" required />
        </div>
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  );
};

export default Register;