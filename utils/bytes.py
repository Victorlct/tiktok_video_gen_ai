# Texto fornecido
texto = [
    "6 Curiosidades Detalhadas sobre Tecnologias Limpas e Sustentáveis:",
    "1. Energia Solar Termodinâmica: Esta tecnologia concentra a luz solar por meio de espelhos ou lentes para aquecer um fluido, que por sua vez gera vapor para alimentar uma turbina que produz eletricidade. É uma das tecnologias de energia renovável mais eficientes, com uma taxa de conversão superior a 50%.",
    "2. Biocombustíveis Avançados: Esses combustíveis são produzidos a partir de fontes vegetais não comestíveis, como algas, plantas celulósicas e resíduos agrícolas. Eles podem substituir os combustíveis fósseis em veículos e indústrias com emissões reduzidas de gases de efeito estufa.",
    "3. Edifícios Verdes: Projetados para minimizar o impacto ambiental, esses edifícios incorporam recursos como isolamento eficiente, sistemas de iluminação natural, telhados verdes e sistemas de gestão de água. Eles podem reduzir significativamente o consumo de energia e as emissões de carbono.",
    "4. Veículos Elétricos: Esses veículos são alimentados por eletricidade armazenada em baterias e não emitem gases de escape. Eles estão se tornando cada vez mais populares devido ao aumento da disponibilidade de estações de carregamento e melhorias na autonomia.",
    "5. Gerenciamento de Resíduos: Tecnologias avançadas, como reciclagem mecânica, compostagem industrial e incineração com recuperação de energia, ajudam a reduzir o desperdício e recuperar recursos valiosos. Isso conserva recursos naturais e reduz as emissões de metano de aterros sanitários.",
    "6. Armazenamento de Energia: Sistemas de armazenamento de energia, como baterias de íons de lítio e armazenamento hidrelétrico bombeado, são cruciais para integrar fontes renováveis intermitentes, como solar e eólica, na rede elétrica. Eles permitem que o excesso de energia seja armazenado para uso posterior, garantindo a confiabilidade e a estabilidade da rede.",
    "Curiosidade Bônus Surpreendente:",
    "Turbina Eólica VTOL (Decolagem e Pouso Verticais): Esta tecnologia inovadora combina turbinas eólicas com rotores de aeronaves para gerar eletricidade enquanto paira no ar. Isso permite que as turbinas sejam implantadas em locais remotos e de difícil acesso, como sobre corpos d'água ou em regiões montanhosas, expandindo potencialmente o aproveitamento do vento."
]

# Convertendo o texto para uma única string
texto_completo = "\n".join(texto)

# Calculando o tamanho em bytes
tamanho_bytes = len(texto_completo.encode("utf-8"))

print(f"O texto tem {tamanho_bytes} bytes.")
