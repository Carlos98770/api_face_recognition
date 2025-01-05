
# api_face_recognition

API para um sistema IoT para reconhecimento facial
-> Atualmente a API não está no ar, é necessário clonar o repositorio e rodar localmente

### Resumo para rodar a API localmente:

1. **Clonar o repositório**.
2. **Criar e ativar o ambiente virtual**.
3. **Atualizar ferramentas essenciais** (`pip`, `setuptools`, `wheel`).
4. **Instalar as dependências** com `pip install -r requirements.txt`.
5. **Executar o servidor** com `python manage.py runserver`.
6. Acessar a rota /api/users e Cadastra um user
7. Acessar a rota /api/users/check Para validação facial. OBS: A imagem tem que está codificada na base64

-> Como o projeto foi pensado para integralização com sistema IoT, a Requisão http que o MIcro Controlador realizará precisa da imagem codificada na base64, logo o algoritmo abaixo realiza a codificação:

1. Certifique-se de que a biblioteca `libb64` está instalada no seu sistema.
2. Salve o código abaixo em um arquivo C, por exemplo `encode_image.c`.

## Código em C

```c
#include <stdio.h>
#include <stdlib.h>
#include "b64/cencode.h" // Biblioteca libb64

void encode_image_to_base64(const char *image_path) {
    FILE *image_file = fopen(image_path, "rb");
    if (!image_file) {
        perror("Erro ao abrir imagem");
        return;
    }

    // Obter tamanho do arquivo
    fseek(image_file, 0, SEEK_END);
    long file_size = ftell(image_file);
    rewind(image_file);

    // Ler imagem para o buffer
    unsigned char *buffer = (unsigned char *)malloc(file_size);
    if (!buffer) {
        perror("Erro ao alocar memória");
        fclose(image_file);
        return;
    }
    fread(buffer, 1, file_size, image_file);
    fclose(image_file);

    // Codificar em Base64
    size_t output_size = ((file_size + 2) / 3) * 4 + 1;
    char *encoded = (char *)malloc(output_size);
    if (!encoded) {
        perror("Erro ao alocar memória para saída");
        free(buffer);
        return;
    }

    base64_encodestate state;
    base64_init_encodestate(&state);
    int output_length = base64_encode_block((const char *)buffer, file_size, encoded, &state);
    output_length += base64_encode_blockend(encoded + output_length, &state);
    encoded[output_length] = '\0';

    printf("%d ", output_length);

    free(buffer);

    // Exibir a string Base64
    //printf("Imagem codificada em Base64:\n%s\n", encoded);
    FILE *outputFile = fopen("output.b64", "w");
    if (outputFile) {
        // Loop para percorrer a string codificada e escrever apenas os caracteres que não são quebras de linha
        for (char *p = encoded; *p; p++) {
            if (*p != '\n') {  // Ignora quebras de linha
                fputc(*p, outputFile);  // Escreve cada caractere no arquivo
            }
        }

        // Fecha o arquivo
        fclose(outputFile);

        // Mensagem de sucesso
        printf("Imagem codificada foi salva em 'output.b64'.\n");
    }
    free(encoded);
}

int main() {
    const char *image_path = "picture4.jpeg";
    encode_image_to_base64(image_path);
    return 0;
}
```
