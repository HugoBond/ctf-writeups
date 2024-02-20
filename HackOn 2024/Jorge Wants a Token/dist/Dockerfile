FROM python:3.11-alpine 

RUN apk add --no-cache socat

WORKDIR /app
RUN pip install pycryptodome ecdsa   
COPY administration.py library.py /app

ENV FLAG="HackOn{I_c4n_s33_b14s3d_N0nc3s_3verywh3r3_I_g0.0nc3_m0r3_s4g3_1s_4lways_4_g00d_fr13nd}"

EXPOSE 1337
CMD ["socat", "TCP-LISTEN:1337,reuseaddr,fork", "EXEC:python administration.py"]
