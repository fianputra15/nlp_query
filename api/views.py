import nltk
import json
from django.shortcuts import render
from rest_framework import status
from .models import Mahasiswa,Freq,Nilai,KelasKata,Understander,JenisKelasKata,TypeQuery
from .serializers import MahasiswaSerializer,FreqSerializer,NilaiSerializer,KelasKataSerializer,NilaiCreateSerializer,JenisKelasKataSerializer,UnderstanderSerializer,TypeQuerySerializer
from rest_framework.decorators import api_view, permission_classes
from django.http import JsonResponse
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

#Master Area
#Mahasiswa
@api_view(["GET","PUT","DELETE","PATCH"])
@csrf_exempt
def mahasiswaOperation(request, id):
    try:
        mahasiswa = Mahasiswa.objects.get(id=id)
    except:
        return JsonResponse(["message","Data Tidak Ditemukan"])
    if request.method == 'GET':
        serializer = MahasiswaSerializer(mahasiswa)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = MahasiswaSerializer(mahasiswa, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        mahasiswa.delete()
        return JsonResponse(safe=False, data=["Data Mahasiswa Berhasil Dihapus"])

@api_view(["POST"])
def mahasiswaAdd(request):
    if request.method == 'POST':
        serializer = MahasiswaSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def mahasiswaAll(request):
    mhs = Mahasiswa.objects.all()
    serializer = MahasiswaSerializer(mhs, many=True)  # convert into JSON
    return JsonResponse(serializer.data, safe=False)

#Freq
@api_view(["GET","PUT","DELETE","PATCH"])
@csrf_exempt
def freqOperation(request, id):
    try:
        freq = Freq.objects.get(id=id)
    except:
        return JsonResponse(["Data Tidak Ditemukan"])
    if request.method == 'GET':
        serializer = FreqSerializer(freq)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = FreqSerializer(freq, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        freq.delete()
        return JsonResponse(safe=False, data=["Data Frekuensi Berhasil Dihapus"])

@api_view(["POST"])
def freqAdd(request):
    if request.method == 'POST':
        serializer = FreqSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(["Data Freq Berhasil Ditambah"],safe=False,status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def freqAll(request):
    freq = Freq.objects.all()
    serializer = FreqSerializer(freq, many=True)  # convert into JSON
    return JsonResponse(serializer.data, safe=False)

#Freq
@api_view(["GET","PUT","DELETE","PATCH"])
@csrf_exempt
def nilaiOperation(request, id):
    try:
        nilai = Nilai.objects.get(id=id)
    except:
        return JsonResponse(["Data Tidak Ditemukan"])
    if request.method == 'GET':
        serializer = NilaiSerializer(nilai)
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        serializer = NilaiCreateSerializer(nilai, data = request.data)
        if(serializer.is_valid()):
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.error_messages, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        nilai.delete()
        return JsonResponse(["Data Mahasiswa Berhasil Dihapus"])

@api_view(["POST"])
def nilaiAdd(request):
    if request.method == 'POST':
        serializer = NilaiCreateSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse(["Data Nilai Berhasil Ditambah"],safe=False,status=status.HTTP_201_CREATED)
    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def nilaiAll(request):
    nilai = Nilai.objects.all()
    serializer = NilaiSerializer(nilai, many=True)  # convert into JSON
    return JsonResponse(serializer.data, safe=False)

#Preprocessing Method
def preProcessing(kalimat):
    #Case Folding
    lower_case = kalimat.lower()

    #Tokenizing
    after_tokenizing = nltk.tokenize.word_tokenize(lower_case)

    #StopWord
    factory = StopWordRemoverFactory()
    get_stopwords = factory.get_stop_words()
    stopword_remover = factory.create_stop_word_remover()
    after_stopword = stopword_remover.remove(' '.join(after_tokenizing))

    #Steeming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    after_stemming = stemmer.stem(after_stopword)

    token = list(after_stemming.split(" "))
    return token

#Untuk menampilkan Preprocessing
def preProcessingWord(kalimat):
    wordPreProcessing = {}
    #Case Folding
    lower_case = kalimat.lower()
    wordPreProcessing['lower_case'] = lower_case
    #Tokenizing
    after_tokenizing = nltk.tokenize.word_tokenize(lower_case)
    wordPreProcessing['tokenizing'] = " - ".join(after_tokenizing)
    #StopWord
    factory = StopWordRemoverFactory()
    get_stopwords = factory.get_stop_words()
    stopword_remover = factory.create_stop_word_remover()
    after_stopword = stopword_remover.remove(' '.join(after_tokenizing))
    wordPreProcessing['stop_word'] =  after_stopword.replace(" "," - ")
    #Steeming
    factory = StemmerFactory()
    stemmer = factory.create_stemmer()
    after_stemming = stemmer.stem(after_stopword)
    wordPreProcessing['stemming'] = after_stemming.replace(" "," - ")
    token = list(after_stemming.split(" "))
    return wordPreProcessing


#Untuk menampilkan Parsing
def parsingProses(token):
    hasil_postag = []
    query_pembentuk = []
    understander = []
    kondisi = []
    kata_sambung = False
    frase_kondisi = ""
    r = ""
    kelas_data = {}
    kelas_data.setdefault("data",{})
    understander_word = ""
    arr_result = ""

    kataperintah = []
    katasambung1 = []
    frasa_atribut = []
    frasa_kondisi = []

    for tokens in token:
        if kata_sambung is False:  #Frase Atribut
            try:
                kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=tokens))
            except KelasKata.DoesNotExist:
                try:
                    understander = UnderstanderSerializer(Understander.objects.get(istilah_lain=tokens))
                    understander_word = understander.data["arti"]
                    try:
                        kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=understander_word))
                    except KelasKata.DoesNotExist:
                        kelaskata = None
                except Understander.DoesNotExist:
                    kelaskata = None
        else:
            kelaskata = None
        if kelaskata is not None: #Kata Sambung
            if kelaskata.data["id_jeniskelaskata"]["namakelas"] == "katasambung1":
                kata_sambung = True
            hasil_postag.append(kelaskata.data)
            print(kelaskata.data["id_jeniskelaskata"]["namakelas"])
        else:
            if kata_sambung is True: #Bagian masih ada bug
                if kelaskata is None:
                    try:
                        kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=tokens))
                    except KelasKata.DoesNotExist:
                        try:
                            understander = UnderstanderSerializer(Understander.objects.get(istilah_lain=tokens))
                            try:
                                kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=understander.data["arti"]))
                            except KelasKata.DoesNotExist:
                                kelaskata = None
                        except Understander.DoesNotExist:
                            understander = None
                    if kelaskata is not None:
                        kondisi.append("-" + kelaskata.data["kata"] + "-")
                    else:
                        kondisi.append(tokens + " ")

    for kt in kondisi:
        frase_kondisi = frase_kondisi + kt

    arr_frasakondisi = frase_kondisi.split("-")
    i = 0
    for i in range(len(arr_frasakondisi)):
        if arr_frasakondisi[i] is not "":
            try:
                kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=arr_frasakondisi[i]))
                hasil_postag.append(kelaskata.data)
            except KelasKata.DoesNotExist:
                try:
                    understander = UnderstanderSerializer(Understander.objects.get(istilah_lain=arr_frasakondisi[i]))
                    arr_frasakondisi[i] = understander.data["arti"]
                except Understander.DoesNotExist:
                    arr_frasakondisi[i] = arr_frasakondisi[i]
                # kelas_data['data'].append(arr_frasakondisi[i])
                arr_result  = arr_result + arr_frasakondisi[i].strip() + ","
                r = {
                    'data' : arr_result.strip()
                }
    r = json.dumps(r)
    kelas_data = json.loads(r)

    #Pembentukan Model Query
    for kk in hasil_postag:
        if kk is not None:
            if 'kataperintah' in kk["id_jeniskelaskata"]["namakelas"]:
                kataperintah.append(kk)
            elif ('namafield' in kk["id_jeniskelaskata"]["namakelas"]) or 'namatabel' in kk["id_jeniskelaskata"]["namakelas"]:
                if len(katasambung1)<=0:
                    frasa_atribut.append(kk)
                else:
                    frasa_kondisi.append(kk)
            elif 'katasambung2' in kk["id_jeniskelaskata"]["namakelas"]:
                if len(katasambung1)>0:
                    frasa_kondisi.append(kk)
            elif 'katasambung1' in kk["id_jeniskelaskata"]["namakelas"]:
                katasambung1.append(kk)
            elif 'atributnilai' in kk["id_jeniskelaskata"]["namakelas"]:
                frasa_kondisi.append(kk)
            elif 'katakuantitas' in kk["id_jeniskelaskata"]["namakelas"]:
                frasa_atribut.append(kk)
    frasa_kondisi.append(kelas_data)
    hasil_postag.append(kelas_data)
    query_pembentuk.extend((kataperintah, frasa_atribut, katasambung1, frasa_kondisi))
    return query_pembentuk




#Untuk Proses Parsing Atau Analisis Sintaksis
def parsing(token):
    hasil_postag = []
    query_pembentuk = []
    understander = []
    kondisi = []
    kata_sambung = False
    frase_kondisi = ""
    r = ""
    kelas_data = {}
    kelas_data.setdefault("data",{})
    understander_word = ""
    arr_result = ""

    kataperintah = []
    katasambung1 = []
    frasa_atribut = []
    frasa_kondisi = []

    for tokens in token:
        if kata_sambung is False:  #Frase Atribut
            try:
                kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=tokens))
            except KelasKata.DoesNotExist:
                try:
                    understander = UnderstanderSerializer(Understander.objects.get(istilah_lain=tokens))
                    understander_word = understander.data["arti"]
                    try:
                        kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=understander_word))
                    except KelasKata.DoesNotExist:
                        kelaskata = None
                except Understander.DoesNotExist:
                    kelaskata = None
        else:
            kelaskata = None
        if kelaskata is not None: #Kata Sambung
            if kelaskata.data["id_jeniskelaskata"]["namakelas"] == "katasambung1":
                kata_sambung = True
            hasil_postag.append(kelaskata.data)
            print(kelaskata.data["id_jeniskelaskata"]["namakelas"])
        else:
            if kata_sambung is True: #Bagian masih ada bug
                if kelaskata is None:
                    try:
                        kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=tokens))
                    except KelasKata.DoesNotExist:
                        try:
                            understander = UnderstanderSerializer(Understander.objects.get(istilah_lain=tokens))
                            try:
                                kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=understander.data["arti"]))
                            except KelasKata.DoesNotExist:
                                kelaskata = None
                        except Understander.DoesNotExist:
                            understander = None
                    if kelaskata is not None:
                        kondisi.append("-" + kelaskata.data["kata"] + "-")
                    else:
                        kondisi.append(tokens + " ")

    for kt in kondisi:
        frase_kondisi = frase_kondisi + kt

    arr_frasakondisi = frase_kondisi.split("-")
    i = 0
    for i in range(len(arr_frasakondisi)):
        if arr_frasakondisi[i] is not "":
            try:
                kelaskata = KelasKataSerializer(KelasKata.objects.get(kata=arr_frasakondisi[i]))
                hasil_postag.append(kelaskata.data)
            except KelasKata.DoesNotExist:
                try:
                    understander = UnderstanderSerializer(Understander.objects.get(istilah_lain=arr_frasakondisi[i]))
                    arr_frasakondisi[i] = understander.data["arti"]
                except Understander.DoesNotExist:
                    arr_frasakondisi[i] = arr_frasakondisi[i]
                # kelas_data['data'].append(arr_frasakondisi[i])
                arr_result  = arr_result + arr_frasakondisi[i].strip() + ","
                r = {
                    'data' : arr_result.strip()
                }
    r = json.dumps(r)
    kelas_data = json.loads(r)

    #Pembentukan Model Query
    for kk in hasil_postag:
        if kk is not None:
            if 'kataperintah' in kk["id_jeniskelaskata"]["namakelas"]:
                kataperintah.append(kk)
            elif 'namafield' in kk["id_jeniskelaskata"]["namakelas"]:
                if len(katasambung1)<=0:
                    frasa_atribut.append(kk)
                else:
                    frasa_kondisi.append(kk)
            elif 'katasambung2' in kk["id_jeniskelaskata"]["namakelas"]:
                if len(katasambung1)>0:
                    frasa_kondisi.append(kk)
            elif 'katasambung1' in kk["id_jeniskelaskata"]["namakelas"]:
                katasambung1.append(kk)
            elif 'atributnilai' in kk["id_jeniskelaskata"]["namakelas"]:
                frasa_kondisi.append(kk)
            elif 'katakuantitas' in kk["id_jeniskelaskata"]["namakelas"]:
                frasa_atribut.append(kk)
    frasa_kondisi.append(kelas_data)
    hasil_postag.append(kelas_data)
    return hasil_postag


# Fungsi Untuk mengecek Frase Kondisi Apakah jamak atau tunggal
def checkFraseKondisi(query_pembentuk):
    kondisifrasekondisi = "" #kondisi untuk frase atribut
    j = 0  # menghitung field pada frasa kondisi
    k = 0  # menghitung atributnilai pada frasa kondisi
    for query in query_pembentuk:
        if (query is not None) and ('data' not in query):
            if 'namafield' in query['id_jeniskelaskata']['namakelas']:
                j += 1
            elif 'atributnilai' in query['id_jeniskelaskata']['namakelas']:
                k += 1
    if (j == 1) and (k < 1):
        kondisifrasekondisi = "fieldtunggal"
    elif (j > 1) and (k < 1):
        kondisifrasekondisi = "fieldjamak"
    elif (j < 1) and (k == 1):
        kondisifrasekondisi = "atributnilaitunggal"
    elif (j < 1) and (k > 1):
        kondisifrasekondisi = "atributnilaijamak"
    elif (j >= 1) and (k >= 1):
        kondisifrasekondisi = "campur"
    else:
        kondisifrasekondisi = ""
    return kondisifrasekondisi

#Fungsi Untuk mengecek Frase Atribut Apakah jamak atau tunggal
def checkFraseAtribut(query_pembentuk):
    kondisifraseatribut = "" #kondisi untuk frase kondisi
    i = 0  # menghitung field pada frasa atribut
    for query in query_pembentuk:
        if (query is not None) and ('data' not in query):
            if 'katakuantitas' in query['id_jeniskelaskata']['namakelas']:
                kondisifraseatribut = "katakuantitas"
            elif 'namafield' in query['id_jeniskelaskata']['namakelas']:
                i += 1

    if i > 1:
        kondisifraseatribut = "fieldjamak"
    elif i == 1:
        kondisifraseatribut = "fieldtunggal"
    return kondisifraseatribut

#Proses Transalation atau Analisis Semantik
def translation(query_pembentuk):
    typequery = "" #menentukan typequery
    frasakondisi = "" #menampung frasa kondisi
    frasaatribut = "" #menampung frasa atribut
    if query_pembentuk[1] != "":
        frasaatribut = checkFraseAtribut(query_pembentuk[1])
    if query_pembentuk[3][0] != "":
        frasakondisi = checkFraseKondisi(query_pembentuk[3])
    else :
        frasakondisi = ""
    if frasaatribut == "katakuantitas":
        if frasakondisi == "":
            typequery = "TYPEQUERY1"
        elif frasakondisi == "fieldtunggal":
            typequery = "TYPEQUERY2"
        elif frasakondisi == "fieldjamak":
            typequery = "TYPEQUERY3"
        elif frasakondisi == "atributnilaitunggal":
            typequery = "TYPEQUERY4"
        elif frasakondisi == "campur":
            typequery = "TYPEQUERY5"
        else:
            typequery = "frasekondisikeliru"
    elif frasaatribut == "fieldtunggal":
        if frasakondisi == "":
            typequery = "TYPEQUERY6"
        elif frasakondisi == "fieldtunggal":
            typequery = "TYPEQUERY7"
        elif frasakondisi == "fieldjamak":
            typequery = "TYPEQUERY8"
        elif frasakondisi == "atributnilaitunggal":
            typequery = "TYPEQUERY9"
        elif frasakondisi == "campur":
            typequery = "TYPEQUERY10"
        else:
            typequery = "frasekondisikeliru"
    elif frasaatribut == "fieldjamak":
        if frasakondisi == "":
            typequery = "TYPEQUERY11"
        elif frasakondisi == "fieldtunggal":
            typequery = "TYPEQUERY12"
        elif frasakondisi == "fieldjamak":
            typequery = "TYPEQUERY13"
        elif frasakondisi == "atributnilaitunggal":
            typequery = "TYPEQUERY14"
        elif frasakondisi == "campur":
            typequery = "TYPEQUERY15"
        else:
            typequery = "frasekondisikeliru"
    else:
        typequery = "fraseatributkeliru"
    return typequery

#Evaluator Method
def evaluatorProses(query_pembentuk):
    data = [] #List Menampung data dari field
    iterable = 0
    j = 0 #Menghitung munculnya field dari mahasiswa
    i = 0 #Menghitung munculnya field dari freq
    hitungfield = 0 #Menghitung field dari mahasiswa dan freq
    mahasiswa_condition = False #validasi untuk kondisi tabel mahasiswa saat query multi table
    freq_condition = False #Validasi untuk kondisi tabel frekuensi saat query multi table
    query_database = "" #Menampung Query Database
    field = [] #Menampung Field Field Yang akan digunakan dalam query
    atribut_nilai = ["mid","hasil"] #menampung atribut nilai
    field_mahasiswa = ["stambuk","nama"] #Field Field yang ada pada tabel mahasiswa
    field_nilai = ["thn_ajaran","nilai"] #Field Field yang ada pada tabel nilai
    field_freq  = ["semester","praktikum","frekuensi"] #Field Field yang ada pada tabel freq
    field_mix = ["nama","frekuensi","stambuk","praktikum","semester"]
    tabel = [] #Berisi Tabel-Tabel yang akan digunakan pada query
    multi_query = False #Menentukan Apakah query termasuk Query Multi Tabel atau belum
    # Mengecek Tabel apa saja yang digunakan di frasa atribut
    for atribut in query_pembentuk[1]:
        if "id_jeniskelaskata" in atribut:
            if atribut['kata'] in field_mahasiswa:
                if "nlp_mahasiswa" not in tabel:
                    tabel.append("nlp_mahasiswa")
            elif atribut['kata'] == "mahasiswa":
                if "nlp_mahasiswa" not in tabel:
                    tabel.append("nlp_mahasiswa")
            elif atribut['kata'] == "freq":
                if "nlp_freq" not in tabel:
                    tabel.append("nlp_freq")
            elif atribut['kata'] == "nilai":
                if "nlp_nilaimahasiswa" not in tabel:
                    tabel.append("nlp_nilaimahasiswa")
            elif (atribut['kata'] in field_freq) or (atribut['kata'] == "kelas") or (atribut['kata'] == "freq"):
                if "nlp_freq" not in tabel:
                    tabel.append("nlp_freq")
            elif atribut['kata'] in field_nilai:
                if "nlp_nilaimahasiswa" not in tabel:
                    tabel.append("nlp_nilaimahasiswa")
    #Mengambil seluruh kata yang ada di frasa kondisi
    for kondisi in query_pembentuk[3]:
        if "id_jeniskelaskata" in kondisi:
            if kondisi['kata'] in field_mahasiswa:
                if "nlp_mahasiswa" not in tabel:
                    tabel.append("nlp_mahasiswa")
            elif (kondisi['kata'] in field_freq) or (kondisi['kata'] == "kelas") or (kondisi['kata'] == "freq"):
                if "nlp_freq" not in tabel:
                    tabel.append("nlp_freq")
            elif kondisi['kata'] in field_nilai:
                if "nlp_nilaimahasiswa" not in tabel:
                    tabel.append("nlp_nilaimahasiswa")
            elif kondisi['kata'] in atribut_nilai:
                if "nlp_nilaimahasiswa" not in tabel:
                    tabel.append("nlp_nilaimahasiswa")

    for kataperintah in query_pembentuk[0]: #Mengambil kataperintah yang ada pada query_pembentuk
        query_database += "Select "
    # Mengambil Frasa atribut yang ada pada query_pembentuk
    for frasaatribut in query_pembentuk[1]:
        if (frasaatribut['kata'] == "semua") or (frasaatribut['kata'] == "seluruh"): #Mengecek Frasa Atribut apakah atribut untuk menampilkan seluruh data
            query_database += "*"
        elif (frasaatribut['kata'] == "total") or (frasaatribut['kata'] == "jumlah") or (frasaatribut['kata'] == "banyak"):  #Mengecek Frasa Atribut apakah atribut menandakan banyaknya data
            query_database += "count(*) as " + frasaatribut['kata'] + " "
        else:
            if frasaatribut['kata'] in field_nilai:
                multi_query = True #Menandakan ini query multi tabel karena berasal dari tabel nilai
                # query_database += " nlp_nilaimahasiswa.nilai,nlp_mahasiswa.nama,nlp_freq.freq fr"
                if frasaatribut['kata'] in field_nilai:
                    field.append("nlp_nilaimahasiswa."+ frasaatribut['kata'])
                    if "nlp_nilaimahasiswa" not in tabel:
                        tabel.append("nlp_nilaimahasiswa")
            else:
                #Mengecek field berasal dari tabel mana di frasa atribut
                if frasaatribut['kata'] in field_mahasiswa:
                    field.append("nlp_mahasiswa." +frasaatribut['kata'])
                    if "nlp_mahasiswa" not in tabel:
                         tabel.append("nlp_mahasiswa")
                elif frasaatribut['kata'] in field_freq:
                    field.append("nlp_freq." + frasaatribut['kata'])
                    if "nlp_freq" not in tabel:
                        tabel.append("nlp_freq")

    #Mengecek apakah query termasuk query multi table atau belum
    if multi_query == True:
        if ('nlp_mahasiswa' not in tabel) and ('nlp_freq' not in tabel): #Mengecek apakah field yang ada tidak termasuk di tabel mahasiswa dan frekuensi
            query_database += ','.join(str(e) for e in field) + " From nlp_nilaimahasiswa where "
        else :
            query_database +=  ','.join(str(e) for e in field) + " From " + ' INNER JOIN '.join(str(e) for e in tabel) #Kalau ada gunakan inner join
            if query_pembentuk[2] != "":
                for frasakatasambung in query_pembentuk[2]:
                    if "katasambung1" in frasakatasambung['id_jeniskelaskata']['namakelas']:
                        query_database += " On " #Memberikan keyword on ketika mendapatkan katasambung1
            if 'nlp_mahasiswa' in tabel:
                if mahasiswa_condition == False: #Mengecek apakah kondisi inner join dari mahasiswa ke nilai sudah ada atau belum
                    if freq_condition == True:
                        if query_pembentuk[3][-1] == "":
                            query_database += " and nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa "
                        else:
                            query_database += " nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa and "
                    else:
                        if query_pembentuk[3][-1] == "":
                            query_database += " on nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa "
                        else:
                            query_database += " nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa and "
                    mahasiswa_condition = True
            if 'nlp_freq' in tabel:
                if freq_condition == False: #Mengecek apakah kondisi inner join dari frekuensi ke nilai sudah ada atau belum
                    if mahasiswa_condition == True:
                        if query_pembentuk[3][-1] == "":
                            query_database += "and nlp_freq.id = nlp_nilaimahasiswa.id_freq"
                        else:
                            query_database += " nlp_freq.id = nlp_nilaimahasiswa.id_freq and "
                    else:
                        if query_pembentuk[3][-1] == "":
                            query_database += "on nlp_freq.id = nlp_nilaimahasiswa.id_freq"
                        else:
                            query_database += " nlp_freq.id = nlp_nilaimahasiswa.id_freq and "
                    freq_condition = True
    else:
        for frasaatribut in query_pembentuk[1]:
            if frasaatribut['kata'] in field_mahasiswa:
                j += 1
            if frasaatribut['kata'] in field_freq:
                i += 1
        if (i>0) and (j>0): #Mengecek apakah field yang ada termasuk di seluruh tabel
            query_database += ','.join(str(e) for e in field) + " From nlp_nilaimahasiswa,nlp_mahasiswa,nlp_freq where nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa and nlp_freq.id = nlp_nilaimahasiswa.id_freq"
            if query_pembentuk[3][-1] != "":
                query_database += " and "
        else:
            query_database +=  ','.join(str(e) for e in field) + " From " + ','.join(str(e) for e in tabel)
            for frasakatasambung in query_pembentuk[2]:
                if "katasambung1" in frasakatasambung['id_jeniskelaskata']['namakelas']:
                    query_database += " Where "

    # if validate_atributnilai == True:
    #     query_database = ("SELECT nlp_mahasiswa.stambuk,nlp_mahasiswa.nama,nlp_nilaimahasiswa.nilai",
    #                       ",nlp_freq.frekuensi,nlp_nilaimahasiswa.praktikum,nlp_nilaimahasiswa.semester,nlp_nilaimahasiswa.thn_ajaran",
    #                       "FROM nlp_mahasiswa A",
    #                       "JOIN nlp_freq B",
    #                       "JOIN nlp_nilaimahasiswa C",
    #                       "ON ")

    #Penngecekan dibagian frasa kondisi untuk dimasukkan di query
    if query_pembentuk[3] != "":
        # Memecah Data Pada Frasa Kondisi
        if "data" in query_pembentuk[3][-1]:
            temp_data = query_pembentuk[3][-1].get("data")[:-1]
            # data = list(temp_data.split(","))
            if temp_data.split(",") is not None:
                data = list(temp_data.split(","))
            else:
                data.append(query_pembentuk[3][-1].get("data")[:-1])
        for frasakondisi in query_pembentuk[3]:
            if "id_jeniskelaskata" in frasakondisi:
                if "katasambung2" in frasakondisi['id_jeniskelaskata']['namakelas']:
                    if frasakondisi['kata'] == "dan":
                        query_database += " and "
                    elif frasakondisi['kata'] == "atau":
                        query_database += " or "
                    elif (frasakondisi['kata'] == "tidak") or (frasakondisi['kata'] == "bukan"):
                        query_database += " not "
                elif "namafield" in frasakondisi['id_jeniskelaskata']['namakelas']:
                    if frasakondisi['kata'] in field_mahasiswa: #Memberikan kondisi dari field mahasiswa
                        query_database += "nlp_mahasiswa." + frasakondisi['kata'] + " = '" + data[iterable] + "' "
                        iterable += 1
                    elif frasakondisi['kata'] in field_nilai:
                        if 'nlp_mahasiswa' in tabel:
                            if mahasiswa_condition == False:
                                query_database += "nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa "
                                mahasiswa_condition = True
                            if multi_query == False:
                                if (mahasiswa_condition == True) or (
                                        freq_condition == True):  # Menambahkan keyword and untuk kondisi terakhir
                                    query_database += " and "
                        if 'nlp_freq' in tabel:
                            if freq_condition == False:
                                query_database += "nlp_freq.id = nlp_nilaimahasiswa.id_freq "
                                freq_condition = True
                            if multi_query == False:
                                if (mahasiswa_condition == True) or (
                                        freq_condition == True):  # Menambahkan keyword and untuk kondisi terakhir
                                    query_database += " and "
                        query_database += "nlp_nilaimahasiswa." + frasakondisi['kata'] + " = '" + data[
                            iterable] + "' "  # Memberikan kondisi dari field nilaimahasiswa
                        iterable += 1
                    elif (frasakondisi['kata'] in field_freq) :
                        query_database += "nlp_freq." + frasakondisi['kata'] + " = '"  + data[iterable] + "' " #Memberikan kondisi dari field frekuensi
                        iterable += 1

                elif "atributnilai" in frasakondisi['id_jeniskelaskata']['namakelas']:
                    # validate_atributnilai = True
                    # if validate_atributnilai == True:
                    #     query_database = ("SELECT nlp_mahasiswa.stambuk,nlp_mahasiswa.nama,nlp_nilaimahasiswa.nilai",
                    #                       ",nlp_freq.frekuensi,nlp_nilaimahasiswa.praktikum,nlp_nilaimahasiswa.semester,nlp_nilaimahasiswa.thn_ajaran",
                    #                       "FROM nlp_mahasiswa A",
                    #                       "JOIN nlp_freq B",
                    #                       "JOIN nlp_nilaimahasiswa C",
                    #                       "ON ")
                    query_database += "nlp_nilaimahasiswa.nilai = " + data[iterable]
                    if 'nlp_mahasiswa' in tabel:
                        if mahasiswa_condition == False:
                            query_database += " and nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa"
                            mahasiswa_condition = True
                    if 'nlp_freq' in tabel:
                        if freq_condition == False:
                            query_database += " and nlp_freq.id = nlp_nilaimahasiswa.id_freq"
                            freq_condition = True
                    iterable += 1
                if multi_query is True:
                    if 'nlp_mahasiswa' in tabel:
                        if mahasiswa_condition == False:
                            query_database += " and nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa"
                            mahasiswa_condition = True
                    if 'nlp_freq' in tabel:
                        if freq_condition == False:
                            query_database += " and nlp_freq.id = nlp_nilaimahasiswa.id_freq"
                            freq_condition = True
    # elif multi_query == True:
    #     query_database += "nlp_mahasiswa.id = nlp_nilaimahasiswa.id_mahasiswa"
    return query_database


#menampilkan hasil Preprocessing
@api_view(["POST"])
def preprocessingProses(request):
    kalimat = preProcessingWord(request.data["kalimat"])
    return JsonResponse(kalimat, safe=False)

#Untuk menampilkan Parsing
@api_view(["POST"])
def parsingWordProses(request):
    kalimat = preProcessing(request.data["kalimat"])
    after_parsing = parsingProses(kalimat)
    # after_translation = translation(after_parsing)
    return JsonResponse(after_parsing, safe=False)

#menampilkan hasil translator
@api_view(["POST"])
def translatorProses(request):
    kalimat = preProcessing(request.data["kalimat"])
    postag = parsingProses(kalimat)
    translator = translation(postag)
    # Mengambil Data Dari Database Untuk TYPEQUERY
    typequery = TypeQuery.objects.get(namatype=translator)
    serializer = TypeQuerySerializer(typequery)
    return JsonResponse(serializer.data, safe=False)

#menampilkan hasil Evaluator
@api_view(["POST"])
def pragmatikProses(request):
    result_evaluator = []
    kalimat = preProcessing(request.data["kalimat"])
    postag = parsingProses(kalimat)
    translator = translation(postag)
    evaluator = evaluatorProses(postag)
    return JsonResponse({'query' : evaluator,'type' : translator}, safe=False)

#Eksekusi Query
def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    desc = cursor.description
    return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
    ]

@api_view(["POST"])
def eksekusiQuery(request):
    kalimat = preProcessing(request.data["kalimat"])
    postag = parsingProses(kalimat)
    evaluator = evaluatorProses(postag)
    cursor = connection.cursor()
    # with connection.cursor() as cursor:
    cursor.execute(evaluator)
    return JsonResponse(dictfetchall(cursor), safe=False)

@api_view(["POST"])
def mainProses(request):
    kalimat = preProcessing(request.POST["kalimat"])
    postag = parsingProses(kalimat)
    return JsonResponse(postag, safe=False)
