from django.db import models

class Mahasiswa(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    stambuk = models.CharField(unique=True,max_length=20)
    nama = models.CharField(max_length=100)
    created_at = models.CharField(max_length=200,blank=True,null=True)
    updated_at = models.CharField(max_length=200,blank=True,null=True)
    class Meta:
        db_table = "nlp_mahasiswa"

class Freq(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    frekuensi = models.CharField(unique=True,max_length=20)
    praktikum = models.CharField(max_length=200)
    semester = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200,blank=True,null=True)
    updated_at = models.CharField(max_length=200,blank=True,null=True)
    class Meta:
        db_table = "nlp_freq"

class Nilai(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    id_mahasiswa = models.ForeignKey(Mahasiswa, on_delete=models.CASCADE,db_column='id_mahasiswa')
    id_freq = models.ForeignKey(Freq, on_delete=models.CASCADE,db_column='id_freq')
    nilai = models.IntegerField()
    thn_ajaran = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200,blank=True,null=True)
    updated_at = models.CharField(max_length=200,blank=True,null=True)
    class Meta:
        db_table = "nlp_nilaimahasiswa"

class JenisKelasKata(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    namakelas = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = "nlp_jeniskelaskata"

class KelasKata(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    kata = models.CharField(max_length=200)
    id_jeniskelaskata = models.ForeignKey(JenisKelasKata, on_delete=models.CASCADE, db_column='id_jeniskelaskata')
    created_at = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = "nlp_kelaskata"

class Understander(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    istilah_lain = models.CharField(max_length=200)
    arti = models.CharField(max_length=200)
    created_at = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = "nlp_understander"

class TypeQuery(models.Model):
    id = models.IntegerField(primary_key=True, max_length=10, blank=True)
    namatype = models.CharField(max_length=200)
    pembentukquery = models.CharField(max_length=200)
    deskripsi = models.CharField(max_length=400)
    created_at = models.CharField(max_length=200, blank=True, null=True)
    updated_at = models.CharField(max_length=200, blank=True, null=True)
    class Meta:
        db_table = "nlp_typequery"