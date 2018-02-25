from __future__ import print_function
import httplib2
import os
import base64
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import RentList, Base
import os
import datetime

now = datetime.datetime.now()

engine = create_engine('sqlite:///tabletennis.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/', methods = ['GET','POST'])
def routeDate():
  sekarang = now.strftime("%Y-%m-%d")
  return redirect('/jadwal/' + sekarang)

@app.route('/jadwal/<date>', methods = ['GET','POST'])
def mainpage(date):
  if request.method == 'GET':
    PeminjamA = session.query(RentList).filter_by(tanggal=date, lapangan='A', status='accepted')
    ListPinjamA = ''
    for i in range(6, 22):
      if (i < 10):
        jam ='0'+str(i)
      else:
        jam =str(i)
      if(PeminjamA.filter_by(jam=jam+'.00').first()):
        if(i < 10):
          ListPinjamA += "<tr><th scope='row'>0"+str(i)+".00</th><td>"+PeminjamA.filter_by(jam=jam+'.00').first().nama+"</td></tr>"
        else :
          ListPinjamA += "<tr><th scope='row'>"+str(i)+".00</th><td>"+PeminjamA.filter_by(jam=jam+'.00').first().nama+"</td></tr>"
      else :
        if(i < 10):
          ListPinjamA += "<tr><th scope='row'>0"+str(i)+".00</th><td>-</td></tr>"
        else :
          ListPinjamA += "<tr><th scope='row'>"+str(i)+".00</th><td>-</td></tr>"
    PeminjamB = session.query(RentList).filter_by(tanggal=date, lapangan='B', status='accepted')
    ListPinjamB= ''
    for i in range(6, 22):
      if(i < 10):
        jam='0'+str(i)
      else:
        jam =str(i)
      if(PeminjamB.filter_by(jam=jam+'.00').first()):
        if(i < 10):
          ListPinjamB += "<tr><th scope='row'>0"+str(i)+".00</th><td>"+PeminjamB.filter_by(jam=jam+'.00').first().nama+"</td></tr>"
        else :
          ListPinjamB += "<tr><th scope='row'>"+str(i)+".00</th><td>"+PeminjamB.filter_by(jam=jam+'.00').first().nama+"</td></tr>"
      else :
        if(i < 10):
          ListPinjamB += "<tr><th scope='row'>0"+str(i)+".00</th><td>-</td></tr>"
        else :
          ListPinjamB += "<tr><th scope='row'>"+str(i)+".00</th><td>-</td></tr>"

    return render_template('jadwal.html', date=date, ListPinjamA=ListPinjamA, ListPinjamB=ListPinjamB)
  else :
    date = request.form['tanggal']
    destination = '/jadwal/' + date
    return redirect(destination)

@app.route('/peminjaman', methods = ['GET','POST'])
def daftar():
  if request.method == 'GET':
    return render_template('sewa.html')
  else : 
    nama = request.form['nama']
    nim = request.form['nim']
    lapangan = request.form['lapangan']
    tanggal = request.form['tanggal']
    jam = request.form['mulai']
    id_line = request.form['line']
    meja = request.form['JumlahMeja']
    net = request.form['JumlahNet']
    bet = request.form['JumlahBet']
    bola1 = request.form['JumlahBola1']
    bola3 = request.form['JumlahBola3']
    lama = request.form['lama']
    total = request.form['hargaTotal']
    status = 'pending'
    jams = jam[0] + jam[1]
    jams = int(jams)
    jamss = jams
    available = True
    if(lama == '0'):
      return ("lama waktu harus > 0")
    for i in range(0, int(lama)):
      jams = jamss + i
      if jams < 10 :
        jam = '0' + str(jams) + '.00'
      else :
        jam = str(jams) + '.00'
      if(session.query(RentList).filter_by(tanggal=tanggal, lapangan=lapangan, jam=jam, status='accepted').first()):
        available = False
        break
      else :
        newEntry = RentList(nama=nama,nim=nim,lapangan=lapangan,tanggal=tanggal,jam=jam,id_line=id_line,meja=meja,net=net,bet=bet,bola1=bola1,bola3=bola3,total=total,status=status, lama=lama)
        session.add(newEntry)
    if(available):
      session.commit()
      if jams-int(lama)+1 < 10 :
        jam = '0' + str(jams-int(lama)+1) + '.00'
      else :
        jam = str(jams-int(lama)+1) + '.00'
      msg = STD_MSG + nama
      kirim = create_message('Peminjaman Meja', 'aditya.farizki1@gmail.com', 'PEMINJAMAN MEJA', msg)
      send_message(get_service(),"me", kirim)
      return render_template('berhasil.html', id=session.query(RentList).filter_by(tanggal=tanggal, lapangan=lapangan, jam=jam, nim=nim).first().id)
    else:
      return render_template('gagal.html')

@app.route('/check', methods = ['GET','POST'])
def check():
  if request.method == 'GET':
    return render_template('check.html')
  else :
    id = request.form['id']
    peminjam = session.query(RentList).filter_by(id=id).first()
    if(peminjam):
      return render_template('check_post.html', id=peminjam.id, nama=peminjam.nama, tanggal=peminjam.tanggal, jam=peminjam.jam, nim=peminjam.nim, total=peminjam.total, status=peminjam.status, lapangan=peminjam.lapangan)
    else:
      return render_template('check_failed.html')

radio_yes = '<label class="rado-inline" for="defaultCheck1" style="color:black;"><input type="radio" name="status{}" value="accepted"  id="defaultCheck1" required>Accept</label>'
radio_no = '<label class="rado-inline" for="defaultCheck1" style="color:black;"><input type="radio" name="status{}" value="declined"  id="defaultCheck1" required>Decline</label>'
radio_del = '<label class="rado-inline" for="defaultCheck1" style="color:black;"><input type="radio" name="status{}" value="delete"  id="defaultCheck1" required>Delete</label>'
btn_submit = '<button class="btn input" type="submit">Submit</button>'

@app.route('/u4tmr380rn', methods= ['GET'])
def approve():
  if request.method == 'GET':
    peminjam = session.query(RentList).filter_by(status='pending').first()
    output = ''
    if (peminjam):
      id = peminjam.id
      peminjam = session.query(RentList).filter_by(status='pending')
      ouput = ''
      for i in range(0, 4):
        peminjam = peminjam.filter_by(id=id).first()
        if (peminjam):
          temp_yes = radio_yes.format(id)
          temp_no = radio_no.format(id)
          temp_del = radio_del.format(id)
          temp_yes = str(temp_yes)
          temp_no = str(temp_no)
          temp_del = str(temp_del)
          output += '<div class="row" style="display:block;text-align:center"><p>Nama = '+peminjam.nama+'</p><p>Nim = '+str(peminjam.nim)+'</p><p>email = '+peminjam.id_line+'</p><p>tanggal = '+peminjam.tanggal+'</p><p>jam = '+peminjam.jam+' lama = '+str(peminjam.lama)+' jam</p><p>lapangan = '+peminjam.lapangan+'</p><p>total = '+peminjam.total+'</p><form action="/u4tmr380rn/'+str(id)+'" method="POST" style="text-align:center">'+temp_yes+temp_no+temp_del+btn_submit+'</form></div>'
          id += peminjam.lama
          peminjam = session.query(RentList).filter_by(status='pending')
        else:
          break
    return render_template('approve.html', output=output)

std_diterima = """<div style="display : block"><p>Request peminjaman meja anda dengan detail</p>
<p> ID = {} </p>
<p> Nama = {}</p>
<p> NIM = {}</p>
<p> Tanggal = {}</p>
<p> Jam = {}</p>
<p> Durasi = {} jam</p>
<p> Biaya = {}</p>
<p> Telah diterima, silahkan datang ke sekre UATM pada waktu yang telah dicantumkan</p>
<h4>Email ini dibuat secara otomatis, jangan membalas email ini</h4></div>"""

std_ditolak = """<div style="display : block"><p>Request peminjaman meja anda dengan detail</p>
<p> ID = {} </p>
<p> Nama = {}</p>
<p> NIM = {}</p>
<p> Tanggal = {}</p>
<p> Jam = {}</p>
<p> Durasi = {} jam</p>
<p> Telah ditolak, Silahkan cek lagi jadwal penggunaan lapangan di situs bit.ly/uatmitbsewa</p>
<h4>Email ini dibuat secara otomatis, jangan membalas email ini</h4></div>"""

@app.route('/u4tmr380rn/<id>', methods= ['POST'])
def post(id):
  status = request.form['status'+str(id)]
  if(status=='accepted'):
    peminjam = session.query(RentList).filter_by(id=id).first()
    lama = peminjam.lama
    for i in range(0,lama):
      peminjam = session.query(RentList).filter_by(id=str(int(id)+i)).first()
      peminjam.status = 'accepted'
    session.commit()
    kirim = create_message('Peminjaman Meja',peminjam.id_line, 'Konfirmasi Peminjaman Meja', std_diterima.format(peminjam.id,peminjam.nama,peminjam.nim,peminjam.tanggal,peminjam.jam,peminjam.lama,peminjam.total))
    send_message(get_service(),"me", kirim)
    return redirect(url_for('approve'))
  elif (status == 'declined'):
    peminjam = session.query(RentList).filter_by(id=id).first()
    lama = peminjam.lama
    for i in range(0,lama):
      peminjam = session.query(RentList).filter_by(id=str(int(id)+i)).first()
      peminjam.status = 'declined'
    session.commit()
    kirim = create_message('Peminjaman Meja',peminjam.id_line, 'Konfirmasi Peminjaman Meja', std_ditolak.format(peminjam.id,peminjam.nama,peminjam.nim,peminjam.tanggal,peminjam.jam,peminjam.lama))
    send_message(get_service(),"me", kirim)
    return redirect(url_for('approve'))
  else:
    peminjam = session.query(RentList).filter_by(id=id).first()
    lama = peminjam.lama
    for i in range(0,lama):
      peminjam = session.query(RentList).filter_by(id=str(int(id)+i)).first()
      session.delete(peminjam)
    session.commit()
    return redirect(url_for('approve'))

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  '''app.debug = True'''
  port = int(os.environ.get('PORT', 80))
  app.run(host='0.0.0.0', port=port)