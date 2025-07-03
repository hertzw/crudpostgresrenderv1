import streamlit as st
from config import  repositorio 


repositorio()
cursor = repositorio.mydb.cursor()

# Streamlit app
def main():
    st.title("CRUD com Postgres")

    # Options
    option=st.sidebar.selectbox("Operação", ("Create", "Read", "Update", "Delete"))

    # Execute operations

    if option=="Create":
        st.subheader("Criação de Registro")
        name=st.text_input("Enter Name")
        email=st.text_input("Enter Email")
        if st.button("Create"):
            sql= "insert into users(name,email) values(%s,%s)"
            val= (name,email)
            repositorio.mysqlcursor.execute(sql,val)
            repositorio.mydb.commit()
            st.success("Registro salvo")

    elif option=="Read":
        st.subheader("Ler Registro")
        repositorio.mysqlcursor.execute("select * from users")
        result = repositorio.mysqlcursor.fetchall()
        for row in result:
            st.write(row)

    elif option=="Update":
        st.subheader("Update a Record")
        id=st.number_input("Enter ID",min_value=1)
        name=st.text_input("Enter New Name")
        email=st.text_input("Enter New Email")
        if st.button("Update"):
            sql="update users set name=%s, email=%s where id =%s"
            val=(name,email,id)
            repositorio.mysqlcursor.execute(sql,val)
            repositorio.mydb.commit()
            st.success("Registro Salvo")

    elif option=="Delete":
        st.subheader("Delete a Record")
        id=st.number_input("Enter ID",min_value=1)
        if st.button("Delete"):
            sql="delete from users where id =%s"
            val=(id,)
            repositorio.mysqlcursor.execute(sql,val)
            repositorio.mydb.commit()
            st.success("Registro removido")

if __name__ == "__main__":
    main()
