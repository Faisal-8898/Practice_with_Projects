<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<html>
  <head>
    <title>Hello this is Faisal here</title>
  </head>
  <body>
    <h2>Welcome, ${name}</h2>
    <h3>Your todos are</h3>
    <table>
      <tbody>
        <c:forEach items="${todos}" var="todo">
          <tr>
            <td>${todo.id}</td>
            <td>${todo.title}</td>
            <td>${todo.description}</td>
          </tr>
        </c:forEach>
      </tbody>
    </table>
  <a href="add-todo">Add Todo</a>
  </body>
</html>
