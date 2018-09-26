# Experimento: JellyFish vs Fat Tree
### Desenvolvido por: José Flauzino

Neste repositório você encontra meus códigos para executar os experimentos que reproduzem a Figura 9 e Tabela 1 do artigo "Jellyfish: Networking Data Centers Randomly".
Saiba mais sobre os objetivos e motivações na <a href="https://github.com/joseflauzino/JellyFish_vs_FatTree/wiki">Wiki do Projeto</a> 

## Obtendo os códigos
1. Verifique se em seu sistema o prgrama git já está instalado com o comando `git`. Caso apareça as informações de ajuda do git é sinal que ele está instalado, caso contrário use o comando a seguir para fazer a instalação: `sudo apt-get update && apt-get install git`.

2. Crie ou escolha um diretório do seu sistema para armazenar os arquivos e entre neste diretório.

3. Faça o clone do repositório no diretório escolhido com o comando `git clone https://github.com/joseflauzino/JellyFish_vs_FatTree`.

## Instalação de pacotes necessários
1. Execute `sudo bash install.sh` para instalar o Ripl e Riplpox

## Para reproduzir a Figura 9

1. Execute `python main.py [N_SWICTHES] [N_LINKS] [N_HOSTS]`, onde [N_SWITCHES] deve ser substituido pelo número de swicthes a rede deve ter, [N_LINKS] é a quantidade de links que cada swicth deve conter e, por fim, [N_HOSTS] é a quantidade de hosts da rede.
2. Exemplo de comando: `python main.py 10 3 4`. Neste caso a rede criada terá 10 switches com 3 conexões cada e 4 hosts na rede.
3. Ao término do processamento a figura estará no diretório /graphics com o nome de acordo com os parâmetros usados no comando. Por exemplo, se o comando foi idêntico ao exemplo do passo 2 o nome da figura será 10sw_3links_4hosts.png. 

<img src="figures/4links_10sw.png" width="450" ></img>

### Possíveis erros
Para ver as soluções de principais erros que podem ocorrer acesse a página de <a href="https://github.com/joseflauzino/JellyFish_vs_FatTree/wiki/Solu%C3%A7ao-de-Poss%C3%ADveis-Erros">Solução de Possíveis Erros</a> na wiki do projeto.

## Para reproduzir a Tabela 1
1. Execute o seguinte comando: `pox/pox.py riplpox.riplpox --topo=jelly,[N_SWITCHES],[N_PORTS],[ADJ_LIST_FILE] --routing=jelly,[ROUTING_FILE] --mode=reactive`

Exemplo de comando para 10 switches com 3 portas cada, lista de adjacencia chamada 'adjList_3links_10sw' e arquivo de rotas chamado 'ecmp_8_3links_10sw'
`pox/pox.py riplpox.riplpox --topo=jelly,10,3,adjList_3links_10sw --routing=jelly,ecmp_8_3links_10sw --mode=reactive`

2. Abra outro terminal e execute `python generate_cmds.py [N_SWITCHES] [N_PORTS] [ADJ_LIST_FILE] [ROUTING_FILE] > [MN_SCRIPT_FILE]`

Exemplo `python generate_cmds.py 10 4 adjList_4links_10sw ecmp_8_4links_10sw > mn_script_ecmp_8_eight_flows`
Obs.: [MN_SCRIPT_FILE] é o nome do arquivo de script Mininet que será criado ao executar o comando, portanto o arquivo não precisa existir (ele será criado).

3. Inicie o Mininet com o comando `sudo mn --custom ripl/ripl/mn.py --topo jelly,[N_SWITCHES],[N_PORTS],[ADJ_LIST_FILE] --link tc --controller=remote --mac`

Exemplo `sudo mn --custom ripl/ripl/mn.py --topo jelly,10,4,adjList_4links_10sw --link tc --controller=remote --mac`

4. Na CLI do Mininet execute `source [MN_SCRIPT_FILE]`
Exemplo `source mn_script_ecmp_8_eight_flows`

5. O resultado estará no diretório outputs/