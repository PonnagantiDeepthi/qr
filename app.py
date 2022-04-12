


from flask import Flask, render_template,request,session,send_file
import uuid
import fitz
import qrcode
import mysql.connector
# from flask_mysqldb import MySQL



 

app = Flask(__name__)
app.secret_key = 'your secret key'

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/pdf_download', methods=['GET', 'POST'])
def d_load():
    out=session['my_var']
    return send_file(out,as_attachment=True)

@app.route('/pdf_qr', methods=['GET', 'POST'])
def working():
    msg=''
    def convertToBinaryData(filename):
        lis= []
        file = open(filename, 'rb').read()
        lis.append(file)
        return lis
   

    def insertBLOB( biodataFile):
        x=uuid.uuid4()
        y=(x.hex)
        print("Inserting BLOB into employee table")
        file = convertToBinaryData(biodataFile)
    
        connection = mysql.connector.connect(host='localhost',database='pythonlogin',user='root',password='Ajay_111')

    
        cursor = connection.cursor()
        cursor.execute('INSERT INTO pdf_files (id,biodata,uniquecode) VALUES (NULL,%s,%s)', (file[0],y))
    
        connection.commit()
   
        print("File inserted successfully as a BLOB into Employee table")
        cursor1 = connection.cursor()
        cursor1.execute('select uniquecode from pdf_files where biodata=%s',file)
        result=cursor1.fetchall()
    
        for i in result:
            print(i[0])
        
        img=qrcode.make(i[0])
        image_file ="firstqr.jpg"
        img.save(image_file)
        
        output_file= "pdf_with_image.pdf"
        image_rectangle = fitz.Rect(0, 0, 51.875, 51.875)

        file_handle = fitz.open(biodataFile)
        first_page = file_handle[0]
        first_page.insertImage(image_rectangle, filename=image_file)
        file_handle.save(output_file)
        msgs ='download the pdf'
        session['my_var'] = output_file
        return (msgs)
    if request.method == 'POST':
        pdffile=request.form['myfile']
      
        msg = insertBLOB(pdffile)
    return render_template('index.html',msg=msg)
if __name__ == "__main__":
    app.run(debug=True)