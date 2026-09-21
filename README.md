# Monitoramento do Estado de Alerta do Motorista - V2

### Sistema baseado em YOLOv8 e Google MediaPipe para monitoramento de distrações ao volante em tempo real.

## Sobre o Projeto

Este projeto apresenta uma solução baseada em **Aprendizado de Máquina** e **Visão Computacional** para monitorar, em tempo real, distrações relacionadas ao uso do telefone celular e sinais de sonolência durante a condução de veículos.

A aplicação integra **YOLOv8** para detecção do telefone celular e **Google MediaPipe Face Mesh** para monitoramento da região dos olhos, permitindo identificar simultaneamente diferentes situações e emitir alertas sonoros e visuais.

Nesta versão, a arquitetura da aplicação foi refatorada com ênfase em **processamento concorrente**, utilizando threads para separar determinadas tarefas do fluxo principal de execução.

---

# Objetivo

Desenvolver um sistema capaz de monitorar o estado de alerta do motorista por meio de técnicas de Visão Computacional, integrando a detecção do uso do celular e de sinais de sonolência com processamento concorrente e controle temporal da aplicação.

---

# Metodologia

A abordagem metodológica utiliza **modelos pré-treinados**, permitindo aproveitar modelos previamente desenvolvidos e treinados em grandes conjuntos de dados.

A solução integra duas tecnologias de Inteligência Artificial:

- **YOLOv8** para detecção do telefone celular;
- **MediaPipe Face Mesh** para monitoramento da região dos olhos e identificação de sinais de sonolência.

A V2 amplia a arquitetura de processamento por meio da utilização de **threads**, permitindo maior separação entre as diferentes tarefas executadas pela aplicação.

Também foi implementado um mecanismo de **controle temporal**, estabelecendo um período de referência para a execução do ciclo principal.

---

# Principais Modificações da V2

A V2 introduz mudanças na arquitetura de processamento da aplicação, com ênfase na **execução concorrente**, **controle temporal** e **modularização do código**.

- **Thread dedicada ao processamento facial:** a análise dos landmarks faciais foi separada do fluxo principal e executada por meio de `threading.Thread`.
- **Processamento concorrente:** maior separação entre as tarefas de captura de vídeo, detecção de objetos, processamento facial e emissão de alertas.
- **Alarmes assíncronos:** os alertas sonoros são executados em threads independentes, evitando que a duração do `Beep` bloqueie diretamente o fluxo principal.
- **Controle temporal:** foi definido um período de referência de `1/30 s`, correspondente a 30 ciclos por segundo.
- **Modularização:** o processamento facial foi transferido para a função `processar_face()`, reduzindo as operações concentradas no loop principal.
- **Centralização dos parâmetros:** período, resolução, limiar de fechamento dos olhos e tempo de fechamento foram definidos no início da aplicação.

---

# Diferenciais da Abordagem

A utilização de **modelos pré-treinados** reduz a necessidade de treinamento de novas redes neurais e permite concentrar o desenvolvimento na integração e no funcionamento da aplicação.

Entre as principais vantagens dessa abordagem estão:

- redução do tempo de desenvolvimento;
- menor necessidade de recursos computacionais para treinamento;
- utilização de modelos previamente treinados;
- facilidade de integração entre diferentes tecnologias;
- concentração dos esforços no desenvolvimento e integração dos módulos da aplicação.

Outro diferencial é a integração entre **YOLOv8 e MediaPipe Face Mesh** em uma única solução, permitindo o monitoramento simultâneo do uso do telefone celular e de sinais de sonolência.

Além da identificação das situações de risco, a aplicação incorpora **alertas sonoros e visuais em tempo real**, permitindo sinalizar imediatamente ao motorista os eventos identificados pelo sistema.

---

# Arquitetura de Processamento

A arquitetura da V2 separa determinadas tarefas do fluxo principal da aplicação por meio da utilização de **threads**.

O fluxo principal permanece responsável pela captura dos frames, processamento do YOLOv8, apresentação dos resultados e controle temporal da aplicação.

O processamento facial é realizado pela função:

```python
processar_face()
```

executada por meio de:

```python
threading.Thread()
```

Os alarmes sonoros também são executados em threads independentes, evitando que o tempo de execução dos sinais sonoros bloqueie diretamente o fluxo principal.

Para o controle temporal, foi estabelecido um período de referência de:

```text
1/30 s ≈ 33,3 ms
```

correspondente a 30 ciclos por segundo.

---

# Funcionamento

O sistema executa continuamente o seguinte fluxo de processamento:

```text
                              Captura de frames de vídeo
                                          │
                                          ▼
                                  Pré-processamento
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  │                                               │
                  ▼                                               ▼
       Detecção do telefone celular                    Processamento facial
                 YOLOv8                                 Thread dedicada
                  │                                               │
                  └───────────────────────┬───────────────────────┘
                                          │
                                          ▼
                                  Módulo de decisão
                                          │
                                          ▼
                                      Resultados
                                          │
                                          ▼
                              Alertas sonoros e visuais
```

---

# Principais Contribuições

- Integração entre YOLOv8 e Google MediaPipe Face Mesh.
- Monitoramento simultâneo do uso do telefone celular e da sonolência.
- Aplicação de processamento concorrente utilizando threads.
- Processamento facial em thread dedicada.
- Execução independente dos alertas sonoros.
- Implementação de controle temporal do ciclo de processamento.
- Refatoração e modularização da arquitetura da aplicação.

---

# Tecnologias Utilizadas

- Python
- OpenCV
- YOLOv8
- Google MediaPipe Face Mesh
- PyTorch
- Threading
- PyCharm

---

# Aplicações

A solução pode ser utilizada em diferentes cenários, tais como:

- Monitoramento de motoristas profissionais;
- Transporte de cargas;
- Sistemas de apoio à condução;
- Pesquisa em Visão Computacional;
- Estudos de processamento concorrente em aplicações de tempo real;
- Estudos relacionados à prevenção de acidentes de trânsito.

---

# Estrutura do Projeto

```text
driving_distraction_detector_v2/

├── images/
├── src/
├── weights/
├── README.md
└── requirements.txt
```

---

# Como Citar / How to Cite

Caso este código ou os resultados desta pesquisa contribuam para o seu trabalho, utilize a seguinte referência:
If this code or the results of this research contribute to your work, please use the following reference:

> Goes, L. S. M., Santos, A. L. C., Da Silva, W. S., & Carvalho, C. B.  
> **Real-Time Driver Distraction Detection with Artificial Intelligence using YOLOv8 and MediaPipe.**  
> *2026 IEEE International Conference on Consumer Electronics (ICCE).* IEEE, 2026.
