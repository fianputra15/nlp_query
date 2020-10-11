from rest_framework import serializers
from .models import Mahasiswa,Freq,Nilai,KelasKata,Understander,JenisKelasKata,TypeQuery


class MahasiswaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mahasiswa
        fields = '__all__'

class FreqSerializer(serializers.ModelSerializer):
    class Meta:
        model = Freq
        fields = '__all__'

class NilaiSerializer(serializers.ModelSerializer):
    id_mahasiswa = MahasiswaSerializer()
    id_freq = FreqSerializer()
    class Meta:
        model = Nilai
        fields = '__all__'

class NilaiCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nilai
        fields = '__all__'

class JenisKelasKataSerializer(serializers.ModelSerializer):
    class Meta:
        model = JenisKelasKata
        fields = '__all__'


class KelasKataSerializer(serializers.ModelSerializer):
    id_jeniskelaskata = JenisKelasKataSerializer()
    class Meta:
        model = KelasKata
        fields = "__all__"

class UnderstanderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Understander
        fields = '__all__'

class TypeQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeQuery
        fields = '__all__'