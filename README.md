## Intro

Esse projeto tem como objetivo converter um video para [ascii art](https://en.wikipedia.org/wiki/ASCII_art).

![grayscale](ascii.gif)

## Requerimentos
Python3.x

## Como funciona?

O projeto consiste em basicamente três partes:

1. Converter os frames do video em imagens
2. Converter as imagens em ascii art
    - Aqui são feitos alguns ajustes nas imagens antes de fazer a conversão para ascii, 
    como resize e normalização dos canais RGB para cinza, ambos para melhorar o desempenho computacional.
    - O algoritmo de conversão em si funciona da seguinte forma: como a imagem já está em escala de cinza, cada pixel
    ocupa 8 bits (1 byte), resultando em 256 escalas de cinza diferentes (2^8), sendo 0 o preto e 255 o branco.
    
         ![grayscale](grayscale.png)
    - A partir disso, a conversão é feita lendo cada valor do pixel e atribuindo um caractere para ele. Por exemplo:
    um pixel possui o valor 10, pelo escala de cinza sabemos que esse pixel se aproxima da cor preta,
    com isso é substituido esse pixel pelo caractere mapeado que mais "se aproxima do preto", no caso, o "@", já
    que ele preenche um grande espaço em relação aos outros caracteres. Outro exemplo pode ser utilizado com 
    um pixel com valor 250, se aproximando do branco e substituindo pelo caractere ".". Essa parte se encontra no método
    *pixels_to_ascii* em *image.py*.
    
3. Converter as imagens de ascii art para video novamente


## Instalando dependências
```
pip install -r requirements.txt
```

## Como usar?

```
python main.py --video-path <path para o video> --threads <OPCIONAL: número de threads. DEFAULT: 1> --fps <OPCINAL: número de fps a ser salvo no vídeo convertido. DEFAULT: 25>
```

