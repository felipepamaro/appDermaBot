# arvoreDecisao.py
# Árvore de decisão – Versão focada em PLACAS (micoses superficiais, líquen simples crônico, psoríase, pitiríase rósea)
# Ordem clínica: Sinais → Histórico → Sintomas → Idade/Sexo (quando pertinente)

ARVORE_DECISAO = {
    "caracteristica": "tipo_lesao_inicial",
    "pergunta": (
        "1) Quais os principais sinais clínicos das lesões identificadas no(a) paciente?\nEx.: placas, lesões eritemato-descamativas, vesículas/bolhas"
    ),
    "ramos": {
        # -----------------------------------------
        # Ramo A — PLACAS
        # -----------------------------------------
        "A": {
            "caracteristica": "caracteristica_micose",
            "pergunta": "As placas são eritematosas apresentando bordas circinadas?",
            "ramos": {
                # ------------------------------------------ 
                # 1) BORDAS CIRCINADAS → Micose superficial
                # ------------------------------------------
                "1": {
                    "caracteristica": "local_micose",
                    "pergunta": "As placas estão localizadas predominantemente nos pés, no tronco ou na virilha?",
                    "ramos": {
                        # SIM para localização típica da micose superficial (bordas + local)
                        "1": {
                            "caracteristica": "tem_prurido_micose",
                            "pergunta": "O(a) paciente relata prurido (coceira)?",
                            "ramos": {
                                # SIM para prurido (bordas + local + prurido)
                                "1": {
                                    "caracteristica": "historico_umidade_micose",
                                    "pergunta": "O(a) paciente utilizou sapatos fechados, roupas quentes/apertadas ou esteve em ambientes úmidos?",
                                    "ramos": {
                                        # SIM para histórico relevante sapatos (bordas + local + prurido + histórico)
                                        "1": {
                                            "folha": {
                                                "dx": "Micoses superficiais (tíneas)",
                                                "justificativa": [
                                                    "Placas eritematosas com bordas circinadas localizadas nos pés, tronco ou virilha em condições favoráveis à proliferação de fungos dermatófitos (ambientes úmidos/sapatos fechados), apresentando sintomas como prurido."
                                                ],
                                                "orientacoes": [
                                                    "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                    "Secar bem a pele após o banho.",
                                                    "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                    "Prefira sapatos abertos, largos e ventilados.",
                                                    "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                ]
                                            }
                                        },
                                        # NÃO para histórico relevante sapatos (bordas + local + prurido - sapatos)
                                        "2": {
                                            "caracteristica": "historico_diabetes_micose",
                                            "pergunta": "O(a) paciente tem histórico de diabetes?",
                                            "ramos": {
                                                # SIM para histórico relevante diabetes (bordas + local + prurido - sapatos + diabetes)
                                                "1": {
                                                    "folha": {
                                                        "dx": "Micoses superficiais — provável",
                                                        "justificativa": [
                                                            "Placas eritematosas com bordas circinadas nos pés, tronco ou virilha com prurido em paciente com histórico de diabetes.",
                                                            "Entretanto, não foi confirmada a exposição a situações que favorecem a proliferação de fungos dermatóficos, como uso de sapatos fechados e ambientes úmidos.",
                                                            "Talvez seja necessário reavaliar as informações do(a) paciente."
                                                        ],
                                                        "orientacoes": [
                                                            "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                            "Secar bem a pele após o banho.",
                                                            "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                            "Prefira sapatos abertos, largos e ventilados.",
                                                            "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                        ]
                                                    }
                                                },
                                                # NÃO para histórico relevante diabates (bordas + local + prurido - sapatos - diabetes)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Micoses superficiais — provável",
                                                        "justificativa": [
                                                            "Placas eritematosas com bordas circinadas localizadas nos pés, tronco ou virilha com prurido.",
                                                            "Entretanto, não foi confirmada a exposição a situações que favorecem a proliferação de fungos dermatóficos, como uso de sapatos fechados e ambientes úmidos.",
                                                            "Paciente também não relatou histórico de diabetes.",
                                                            "Talvez seja necessário reavaliar as informações do(a) paciente."
                                                        ],
                                                        "orientacoes": [
                                                            "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                            "Secar bem a pele após o banho.",
                                                            "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                            "Prefira sapatos abertos, largos e ventilados.",
                                                            "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                # NÃO para prurido (bordas + local - prurido)
                                "2": {
                                    "caracteristica": "historico_umidade_micose",
                                    "pergunta": "Entendi, sem prurido. O(a) paciente utilizou sapatos fechados, roupas quentes/apertadas ou teve contato com ambientes úmidos?",
                                    "ramos": {
                                        # SIM para histórico sapatos (bordas + local - prurido + histórico sapatos)
                                        "1": {
                                            "folha": {
                                                "dx": "Micoses superficiais — possível",
                                                "justificativa": [
                                                    "Placas eritematosas com bordas circinadas localizadas nos pés, tronco ou virilha em condições favoráveis à proliferação de fungos dermatófitos (ambientes úmidos/sapatos fechados).",
                                                    "Entretanto, não foi confirmada a presença de prurido. Como o prurido é o principal sintoma da micose superficial, é necessário rever as informações do(a) paciente."
                                                ],
                                                "orientacoes": [
                                                    "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                    "Secar bem a pele após o banho.",
                                                    "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                    "Prefira sapatos abertos, largos e ventilados.",
                                                    "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                ]
                                            }
                                        },
                                        # NÃO para histórico sapatos (bordas + local - prurido - histórico sapatos)
                                        "2": {
                                            "caracteristica": "historico_diabetes_micose",
                                            "pergunta": "O(a) paciente tem histórico de diabetes?",
                                            "ramos": {
                                                # SIM para histórico diabetes (bordas + local - prurido - histórico sapatos + histórico diabetes)
                                                "1": {
                                                    "folha": {
                                                        "dx": "Micoses superficiais — provável",
                                                        "justificativa": [
                                                            "Placas eritematosas com bordas circinadas localizadas nos pés, tronco ou virilha em paciente com histórico de diabetes.",
                                                            "Entretanto, não foi confirmada a exposição a situações que favorecem a proliferação de fungos dermatóficos, como uso de sapatos fechados e ambientes úmidos.",
                                                            "Também não foi confirmada a presença de prurido, sendo este o principal sintoma da micose superficial.",
                                                            "Além disso, o paciente não apresenta histórico de diabetes. É necessário rever as informações do(a) paciente."
                                                        ],
                                                        "orientacoes": [
                                                            "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                            "Secar bem a pele após o banho.",
                                                            "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                            "Prefira sapatos abertos, largos e ventilados.",
                                                            "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                        ]
                                                    }
                                                },
                                                # NÃO para histórico diabetes (bordas + local - prurido - histórico sapatos - histórico diabetes)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Micose superficial — considerar; diagnóstico ainda inconclusivo",
                                                        "justificativa": [
                                                            "Placas eritematosas com bordas circinadas localizadas nos pés, tronco ou virilha.",
                                                            "Entretanto, não foi confirmada a exposição a situações que favorecem a proliferação de fungos dermatóficos, como uso de sapatos fechados e ambientes úmidos.",
                                                            "Também não foi confirmada a presença de prurido, sendo este o principal sintoma da micose superficial.",
                                                            "Além disso, o paciente não apresenta histórico de diabetes."
                                                        ],
                                                        "orientacoes": [
                                                            "Reavaliar evolução; exame micológico se possível."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        # NÃO para localização típica (bordas - local)
                        "2": {
                            "caracteristica": "tem_prurido_micose",
                            "pergunta": "O(a) paciente relata prurido (coceira)?",
                            "ramos": {
                                # SIM para prurido (bordas - local + prurido)
                                "1": {
                                    "caracteristica": "historico_umidade_micose",
                                    "pergunta": "O(a) paciente utilizou sapatos fechados, roupas quentes/apertadas ou teve contato com ambientes úmidos?",
                                    "ramos": {
                                        # SIM para histórico sapatos (bordas - local + prurido + histórico sapatos)
                                        "1": {
                                            "folha": {
                                                "dx": "Micose superficial - possível",
                                                "justificativa": [
                                                    "Placas eritematosas com bordas circinadas com prurido em condições favoráveis à proliferação de fungos dermatófitos (ambientes úmidos/sapatos fechados).",
                                                    "Apesar das regiões onde se localizam as placas não serem comuns da micose superficial, isso não descarta a hipótese da doença."
                                                ],
                                                "orientacoes": [
                                                    "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                    "Secar bem a pele após o banho.",
                                                    "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                    "Prefira sapatos abertos, largos e ventilados.",
                                                    "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                ]
                                            }
                                        },
                                        # NÃO para histórico sapatos (bordas - local + prurido - histórico sapatos)
                                        "2": {
                                            "caracteristica": "historico_diabetes_micose",
                                            "pergunta": "O(a) paciente tem histórico de diabetes?",
                                            "ramos": {
                                                # SIM para histórico diabetes (bordas - local + prurido - histórico sapatos + histórico diabetes)
                                                "1": {
                                                    "folha": {
                                                        "dx": "Micose superficial - provável",
                                                        "justificativa": [
                                                            "Placas eritematosas com bordas circinadas com prurido em pacientes com diabetes sugerem micose superficial.",
                                                            "Apesar das regiões onde se localizam as placas não serem comuns da micose superficial, isso não descarta a hipótese da doença."
                                                        ],
                                                        "orientacoes": [
                                                            "Usar cremes antifúngicos ou medicamentos orais dependendo da gravidade e do tipo de infecção.",
                                                            "Secar bem a pele após o banho.",
                                                            "Evitar tecidos sintéticos e roupas quentes e apertadas.",
                                                            "Prefira sapatos abertos, largos e ventilados.",
                                                            "Evite andar descalço em locais úmidos como vestiários e saunas."
                                                        ]
                                                    }
                                                },
                                                # NÃO para histórico diabetes (bordas - local + prurido - histórico sapatos - histórico diabetes)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Micose superficial - considerar; diagnóstico ainda inconclusivo.",
                                                        "justificativa": [
                                                            "Placas eritematosas com bordas circinadas com prurido sugerem micose superficial",
                                                            "Entretanto, não foi confirmada a exposição a situações que favorecem a proliferação de fungos dermatóficos, como uso de sapatos fechados e ambientes úmidos.",
                                                            "As regiões das placas não são típicas de micose e o(a) paciente não apresenta histórico de diabetes."
                                                        ],
                                                        "orientacoes": [
                                                            "Reavaliar evolução; exame micológico se possível."
                                                        ]
                                                    }
                                                }
                                            }
                                        }   
                                    }
                                },
                                # NÃO para prurido (bordas - local - prurido)
                                "2": {
                                    "folha": {
                                        "dx": "Micose superficial - considerar; diagnóstico ainda inconclusivo.",
                                        "justificativa": [
                                            "Placas eritematosas com bordas circinadas são características da micose superficial.",
                                            "Porém, não foi confirmada a presença de prurido, sendo este o principal sintoma da micose superficial.",
                                            "Não foi confirmada a exposição a situações que favorecem a proliferação de fungos dermatóficos, como uso de sapatos fechados e ambientes úmidos.",
                                            "Apesar das regiões onde se localizam as placas não serem comuns da micose superficial, isso não descarta a hipótese da doença."
                                        ],
                                        "orientacoes": [
                                            "Reavaliar evolução; exame micológico se possível."
                                        ]
                                    }
                                }
                            }
                        }
                    }
                },

                # 2) NÃO TEM bordas circinadas --> Líquen simples crônico / Psoríase / Pitiríase rósea
                "2": {
                    "caracteristica": "caracteristica_liquen",
                    "pergunta": "As placas são liquenificadas?",
                    "ramos": {
                        # -----------------------------------------------------
                        # PLACAS LIQUENIFICADAS --> Líquen simples crônico
                        # -----------------------------------------------------
                        "1": {
                            "caracteristica": "local_liquen",
                            "pergunta": (
                                "As placas se concentram em alguma dessas regiões?\n",
                                "- Nuca\n",
                                "- Região sacra\n",
                                "- Genitais\n",
                                "- Membros (inferiores e/ou superiores)"
                            ),
                            "ramos": {
                                # SIM local típico liquen (liquenificada + local)
                                "1": {
                                    "caracteristica": "tem_prurido_liquen",
                                    "pergunta": "O(a) paciente relata prurido?",
                                    "ramos": {
                                        # SIM prurido (liquenificada + local + prurido)
                                        "1": {
                                            "caracteristica": "historico_liquen",
                                            "pergunta": (
                                                "O paciente relatou algum dos históricos abaixo?\n",
                                                "- Estresse e/ou ansiedade\n",
                                                "- Atopia\n",
                                                "- Dermatite\n",
                                                "- Picadas de inseto\n"
                                            ),
                                            "ramos": {
                                                # SIM histórico liquen (liquenificada + local + prurido + histórico)
                                                "1": {
                                                    "folha": {
                                                        "dx": "Líquen simples crônico",
                                                        "justificativa": [
                                                            "Presença de placas liquenificadas, prurido, localização e histórico condizentes com líquen simples crônico.",
                                                        ],
                                                        "orientacoes": [
                                                            "Parar o ciclo de coçar e arranhar.",
                                                            "Uso de cremes e pomadas de corticosteroides tópicos, hidratantes e, em alguns casos, medicamentos orais.",
                                                            "É fundamental identificar e evitar gatilhos, como estresse e irritantes."
                                                        ]
                                                    }     
                                                },
                                                # NÃO histórico líquen (liquenificada + local + prurido - histórico)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Líquen simples crônico - possível",
                                                        "justificativa": [
                                                                "Presença de placas liquenificadas, prurido e localização condizentes com líquen simples crônico.",
                                                                "A falta de histórico relevante para o líquen, não descarta a doença devido aos outros relatos."
                                                        ],
                                                        "orientacoes": [
                                                            "Parar o ciclo de coçar e arranhar.",
                                                            "Uso de cremes e pomadas de corticosteroides tópicos, hidratantes e, em alguns casos, medicamentos orais.",
                                                            "É fundamental identificar e evitar gatilhos, como estresse e irritantes."
                                                        ]     
                                                    }
                                                }
                                            }
                                        },
                                        
                                        # NÃO prurido (liquenificada + local - prurido)
                                        "2": {
                                            "folha": {
                                                "dx": "Líquen simples crônico - considerar; diagnóstico ainda inconclusivo",
                                                "justificativa": [
                                                    "A presença de placas liquenificadas na região indicada sugere líquen simples crônico.",
                                                    "Porém, a mesma é caracterizada pelo prurido persistente (ciclo coça-coça).",
                                                    "A ausência de prurido faz com que seja necessário reavaliar o paciente."
                                                ],
                                                "orientacoes": [
                                                    "Reavaliar os sintomas do paciente."
                                                ] 
                                            }
                                        }
                                    }
                                },

                                # NÃO local típico liquen (liquenificada - local)
                                "2": {
                                    "caracteristica": "tem_prurido_liquen",
                                    "pergunta": "O(a) paciente relata prurido?",
                                    "ramos": {
                                        # SIM prurido (liquenificada - local + prurido)
                                        "1": {
                                            "caracteristica": "historico_liquen",
                                            "pergunta": (
                                                "O paciente relatou algum dos históricos abaixo?\n",
                                                "- Estresse e/ou ansiedade\n",
                                                "- Atopia\n",
                                                "- Dermatite\n",
                                                "- Picadas de inseto"
                                            ),
                                            "ramos": {
                                                # SIM histórico liquen (liquenificada - local + prurido + histórico)
                                                "1": {
                                                    "folha": {
                                                        "dx": "Líquen simples crônico - possível",
                                                        "justificativa": [
                                                            "Presença de placas liquenificadas, prurido e histórico condizentes com líquen simples crônico.",
                                                            "Embora a localização das placas não seja típica de líquen simples crônico, os outros relatos sugerem fortemente a doença."
                                                        ],
                                                        "orientacoes": [
                                                            "Parar o ciclo de coçar e arranhar.",
                                                            "Uso de cremes e pomadas de corticosteroides tópicos, hidratantes e, em alguns casos, medicamentos orais.",
                                                            "É fundamental identificar e evitar gatilhos, como estresse e irritantes."
                                                        ]
                                                    }     
                                                },
                                                # NÃO histórico líquen (liquenificada - local + prurido - histórico)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Líquen simples crônico - provável",
                                                        "justificativa": [
                                                            "Presença de placas liquenificadas com prurido sugerem líquen simples crônico.",
                                                            "A falta de histórico relevante para o líquen e a localização não-típica, não descartam a doença se houver prurido persistente com ciclo coça-coça."
                                                        ],
                                                        "orientacoes": [
                                                            "Parar o ciclo de coçar e arranhar.",
                                                            "Uso de cremes e pomadas de corticosteroides tópicos, hidratantes e, em alguns casos, medicamentos orais.",
                                                            "É fundamental identificar e evitar gatilhos, como estresse e irritantes."
                                                        ]     
                                                    }
                                                }
                                            }
                                        },
                                         # NÃO prurido (liquenificada - local - prurido)
                                        "2": {
                                            "folha": {
                                                "dx": "Líquen simples crônico - considerar; diagnóstico ainda inconclusivo",
                                                "justificativa": [
                                                    "A presença de placas liquenificadas é caracteristica do líquen simples crônico.",
                                                    "Porém, a mesma é caracterizada pelo prurido persistente (ciclo coça-coça).",
                                                    "A ausência de prurido faz com que seja necessário reavaliar o paciente."
                                                ],
                                                "orientacoes": [
                                                    "Reavaliar os sintomas do paciente."
                                                ] 
                                            }
                                        }
                                    }   
                                }
                            }
                        },

                        # NÃO placas liquenificadas --> Psoríase / Pitiríase rósea
                        "2": {
                            "caracteristica": "caracteristica_psoriase",
                            "pergunta": "As placas são eritemato-descamativas apresentando bordas bem definidas?",
                            "ramos": {
                                # --------------------------------
                                # BORDAS BEM DEFINIDAS --> PSORÍASE
                                # --------------------------------
                                "1": {
                                   "caracteristica": "local_psoriase",
                                   "pergunta": "As placas acometem alguma dessas regiões?\n- Couro cabeludo\n- Joelhos e/ou cotovelos",
                                   "ramos": {
                                        # SIM local psoríase (bordas bem definidas + local)
                                        "1": {
                                            "caracteristica": "tem_prurido_psoriase",
                                            "pergunta": "O(a) paciente relatou prurido (coceira)?",
                                            "ramos": {
                                                # SIM prurido (bordas bem definidas + local + prurido)
                                                "1": {
                                                    "caracteristica": "historico_psoriase",
                                                    "pergunta": "O(a) paciente relatou histórico de estresse?",
                                                    "ramos": {
                                                        # SIM histórico estresse (bordas bem definidas + local + prurido + histórico)
                                                        "1": {
                                                            "folha": {
                                                                "dx": "Psoríase",
                                                                "justificativa": [
                                                                    "Placas eritemato-descamativas com bordas bem definidas, prurido, localização condizente e histórico relevante"
                                                                ],
                                                                "orientacoes": [
                                                                    "Manter a pele hidratada com cremes específicos.",
                                                                    "Evitar estresse e o consumo de álcool/tabagismo",
                                                                    "Ter uma alimentação saudável e balanceada"
                                                                ] 
                                                            }          
                                                        },
                                                        # NÃO histórico estresse (bordas bem definidas + local + prurido - histórico)
                                                        "2": {
                                                            "folha": {
                                                                "dx": "Psoríase - possível",
                                                                "justificativa": [
                                                                    "Placas eritemato-descamativas com bordas bem definidas, prurido e localização condizente.",
                                                                    "Mesmo não apresentando histórico de estresse, o diagnóstico de psoríase ainda é possível."
                                                                ],
                                                                "orientacoes": [
                                                                    "Manter a pele hidratada com cremes específicos.",
                                                                    "Evitar estresse e o consumo de álcool/tabagismo",
                                                                    "Ter uma alimentação saudável e balanceada"
                                                                ] 
                                                            }     
                                                        }
                                                    }      
                                                },
                                                
                                                # NÃO prurido (bordas bem definidas + local - prurido)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Psoríase - considerar; diagnóstico ainda inconclusivo",
                                                        "justificativa": [
                                                            "Placas eritemato-descamativas com bordas bem definidas e localização condizente.",
                                                            "Entretanto, não há relato de prurido, sendo este o principal sintoma de psoríase."
                                                        ],
                                                        "orientacoes": [
                                                            "Reavaliar o paciente."
                                                        ] 
                                                    }  
                                                }
                                            }
                                        },
                                        
                                        # NÃO local psoríase (bordas bem definidas - local)
                                        "2": {
                                            "caracteristica": "tem_prurido_psoriase",
                                            "pergunta": "O(a) paciente relatou prurido (coceira)?",
                                            "ramos": {
                                                # SIM prurido (bordas bem definidas - local + prurido)
                                                "1": {
                                                    "caracteristica": "historico_psoriase",
                                                    "pergunta": "O(a) paciente relatou histórico de estresse?",
                                                    "ramos": {
                                                        # SIM histórico estresse (bordas bem definidas - local + prurido + histórico)
                                                        "1": {
                                                            "folha": {
                                                                "dx": "Psoríase - possível",
                                                                "justificativa": [
                                                                    "Placas eritemato-descamativas com bordas bem definidas, prurido e histórico relevante",
                                                                    "Embora as regiões afetadas não sejam típicas de psoríase, isso não descarta a doença."
                                                                ],
                                                                "orientacoes": [
                                                                    "Manter a pele hidratada com cremes específicos.",
                                                                    "Evitar estresse e o consumo de álcool/tabagismo",
                                                                    "Ter uma alimentação saudável e balanceada"
                                                                ] 
                                                            }          
                                                        },
                                                        # NÃO histórico estresse (bordas bem definidas - local + prurido - histórico)
                                                        "2": {
                                                            "folha": {
                                                                "dx": "Psoríase - provável",
                                                                "justificativa": [
                                                                    "Placas eritemato-descamativas com bordas bem definidas e prurido são características de psoríase.",
                                                                    "Entretanto, devido às regiões indicadas e a falta de histórico relevante, sugere-se reavaliar o paciente com calma."
                                                                ],
                                                                "orientacoes": [
                                                                    "Reavaliar o paciente. Se considerar psoríase:"
                                                                    "Manter a pele hidratada com cremes específicos.",
                                                                    "Evitar estresse e o consumo de álcool/tabagismo",
                                                                    "Ter uma alimentação saudável e balanceada"
                                                                ] 
                                                            }     
                                                        } 
                                                    }
                                                },
                                                
                                                # NÃO prurido (bordas bem definidas - local - prurido)
                                                "2": {
                                                    "folha": {
                                                        "dx": "Psoríase - considerar; diagnóstico ainda inconclusivo",
                                                        "justificativa": [
                                                            "Placas eritemato-descamativas com bordas bem definidas são características de psoríase.",
                                                            "Entretanto, devido às regiões indicadas e a falta de prurido, sugere-se reavaliar o paciente com calma."
                                                        ],
                                                        "orientacoes": [
                                                            "Reavaliar o paciente."
                                                        ] 
                                                    }       
                                                }        
                                            }
                                        }
                                   }
                                },

                                # NÃO bordas bem definidas --> Pitiríase rósea
                                "2": {
                                    "caracteristica": "caracteristica_pitiriase_rosea",
                                    "pergunta": "As placas são eritemato-descamativas com placa-mãe oval e erupções secundárias em tronco?",
                                    "ramos": {
                                        # -----------------------------------
                                        # PLACA-MÃE OVAL --> PITIRÍASE RÓSEA
                                        # -----------------------------------
                                        "1": {
                                            "caracteristica": "infeccao_viral_pitiriase",
                                            "pergunta": "O(a) paciente teve infecção viral prévia?",
                                            "ramos": {
                                                # SIM infecção viral (característica + infecção viral)    
                                                "1": {
                                                    "caracteristica": "local_pitiriase",
                                                    "pergunta": "As placas se concentram no tronco do paciente?",
                                                    "ramos": {
                                                        # SIM tronco (característica + infecção + local)
                                                        "1": {
                                                            "caracteristica": "tem_prurido_pitiriase",
                                                            "pergunta": "Há prurido (coceira)?",
                                                            "ramos": {
                                                                # SIM prurido (característica + infecção + local + prurido)
                                                                "1": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco + prurido + localização condizente + infecção prévia"
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Tomar banhos mornos, usar hidratantes sem fragrância, aplicar loções de calamina ou cremes de corticoides suaves sem receita para a coceira.",
                                                                            "Protejer a pele do sol com roupas largas ou protetor solar."
                                                                        ] 
                                                                    }
                                                                },

                                                                # NÃO prurido (características + infecção + local - prurido)
                                                                "2": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - possível",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco + localização condizente + infecção prévia",
                                                                            "Não há relatos de prurido, o que é incomum. Verificar os sintomas com o paciente."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Tomar banhos mornos, usar hidratantes sem fragrância, aplicar loções de calamina ou cremes de corticoides suaves sem receita para a coceira.",
                                                                            "Protejer a pele do sol com roupas largas ou protetor solar."
                                                                        ] 
                                                                    }
                                                                }
                                                            }

                                                        },
                                                        
                                                        # NÃO tronco (característica + infecção - local)
                                                        "2": {
                                                            "caracteristica": "tem_prurido_pitiriase",
                                                            "pergunta": "Há prurido (coceira)?",
                                                            "ramos": {
                                                                # SIM prurido (característica + infecção - local + prurido)
                                                                "1": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - possível",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco + prurido + infecção prévia.",
                                                                            "Embora a localização não seja a típica da doença, isso não a descarta."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Tomar banhos mornos, usar hidratantes sem fragrância, aplicar loções de calamina ou cremes de corticoides suaves sem receita para a coceira.",
                                                                            "Protejer a pele do sol com roupas largas ou protetor solar."
                                                                        ] 
                                                                    }
                                                                },

                                                                # NÃO prurido (característica + infecção - local - prurido)
                                                                "2": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - provável",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco com infecção viral prévia sugerem pitiríase rósea.",
                                                                            "Entretanto, não há prurido, o que não é a regra.",
                                                                            "Embora a localização não seja a típica da doença, isso não a descarta."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Tomar banhos mornos, usar hidratantes sem fragrância, aplicar loções de calamina ou cremes de corticoides suaves sem receita para a coceira.",
                                                                            "Protejer a pele do sol com roupas largas ou protetor solar."
                                                                        ] 
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }     
                                                },

                                                # NÃO infecção viral (característica - infecção)
                                                "2": {
                                                    "caracteristica": "local_pitiriase",
                                                    "pergunta": "As placas se concentram no tronco do paciente?",
                                                    "ramos": {
                                                        # SIM tronco (característica - infecção + local)
                                                        "1": {
                                                            "caracteristica": "tem_prurido_pitiriase",
                                                            "pergunta": "Há prurido (coceira)?",
                                                            "ramos": {
                                                                # SIM prurido (característica - infecção + local + prurido)
                                                                "1": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - possível",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco + prurido + localização condizente.",
                                                                            "Não houve relato de infecção viral prévia. Reavalie essa informação."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Tomar banhos mornos, usar hidratantes sem fragrância, aplicar loções de calamina ou cremes de corticoides suaves sem receita para a coceira.",
                                                                            "Protejer a pele do sol com roupas largas ou protetor solar."
                                                                        ] 
                                                                    }
                                                                },

                                                                # NÃO prurido (característica - infecção + local - prurido)
                                                                "2": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - provável",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco com localização condizente.",
                                                                            "Entretanto, não há prurido, o que não é a regra.",
                                                                            "Não há relato de infecção viral prévia, o que também dificulta o diagnóstico."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Reavaliar paciente. Caso pitiríase:"
                                                                            "Tomar banhos mornos, usar hidratantes sem fragrância, aplicar loções de calamina ou cremes de corticoides suaves sem receita para a coceira.",
                                                                            "Protejer a pele do sol com roupas largas ou protetor solar."
                                                                        ] 
                                                                    }
                                                                }
                                                            }
                                                        },

                                                        # NÃO tronco (característica - infecção - local)
                                                        "2": {
                                                            "caracteristica": "tem_prurido_pitiriase",
                                                            "pergunta": "Há prurido (coceira)?",
                                                            "ramos": {
                                                                # SIM prurido (característica - infecção - local + prurido)
                                                                "1": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - considerar; diagnóstico ainda inconclusivo",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco + prurido",
                                                                            "Verificar localização e infecção viral prévia para diagnóstico mais preciso."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Reavaliar o paciente."
                                                                        ] 
                                                                    }
                                                                },
                                                                # NÃO prurido (característica - infecção - local - prurido)
                                                                "2": {
                                                                    "folha": {
                                                                        "dx": "Pitiríase rósea - considerar; diagnóstico ainda inconclusivo",
                                                                        "justificativa": [
                                                                            "Placas eritemato-descamativas com placa-mãe oval e erupções em tronco são características de pitiríase rósea.",
                                                                            "Entretanto, não há prurido e as regiões não são condizentes.",
                                                                            "Não há relato de infecção viral prévia, o que também dificulta o diagnóstico."
                                                                        ],
                                                                        "orientacoes": [
                                                                            "Reavaliar paciente."
                                                                        ] 
                                                                    }
                                                                }
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },

                                        # NENHUM caracteristica das placas se encaixam --> sem diagnóstico
                                        "2": {
                                            "folha": {
                                                "dx": "Não é possível dar um diagnóstico.",
                                                "justificativa": [
                                                    "Se as placas identificadas não se encaixam em nenhuma das descrições documentadas, então muito provavelmente não são placas."
                                                ],
                                                "orientacoes": [
                                                    "Reavalie os sinais clínicos das lesões e vamos recomeçar.",
                                                ]
                                            }
                                        }
                                    }
                                }
                            }    
                        }
                    }
                }
            }
        },

        # ----------------------------------
        # RAMO B - LESOES
        # ----------------------------------
        "B": {
            "caracteristica": "local_lesao_disseminada",
            "pergunta": "As lesões estão espalhadas pelo corpo do(a) paciente?",
            "ramos": {
                # SIM lesões eritemato-descamativas espalhadas --> sugerem ERITRODERMIA ESFOLIATIVA / ERITEMA MULTIFORME
                "1": {
                    "caracteristica": "caracteristica_lesao_seca",
                    "pergunta": "A lesão é seca e esfoliativa?",
                    "ramos": {
                        # SIM seca e esfoliativa --> ERITRODERMIA ESFOLIATIVA
                        "1": {
                            "folha": {
                                "dx": "Eritrodermia esfoliativa",
                                "justificativa": [
                                    "Lesões eritemato-descamativas, secas e esfoliativas disseminadas pelo corpo do paciente são clássicas da eritrodermia esfoliativa."
                                ],
                                "orientacoes": [
                                    "Hidratação e nutrição: Beba bastante líquido para repor a perda de fluidos e eletrólitos. Mantenha uma dieta rica em proteínas para suprir a perda excessiva de proteínas pela descamação.",
                                    "Evite desencadeadores conhecidos e irritantes, como medicamentos, se suspeitar que a condição é causada por eles.",
                                    "Tome banhos mornos ou use compressas mornas para acalmar a pele. Evite banhos muito quentes.",
                                    "Use emolientes suaves para hidratar a pele.",
                                    "Mantenha a pele limpa e protegida.",
                                    "Podem ser usados corticoides (sistêmicos ou tópicos), antibióticos (para infecções), anti-histamínicos para coceira e, dependendo da causa, outros tratamentos específicos como fototerapia."
                                ]
                            }
                        },
                        # NÃO seca e esfoliativa --> sugere ERITEMA MULTIFORME
                        "2": {
                            "caracteristica": "caracteristica_lesao_alvo",
                            "pergunta": "As lesões apresentam-se em alvo, podendo ter vesículas?",
                            "ramos": {
                                # SIM lesões em alvo --> ERITEMA MULTIFORME
                                "1": {
                                    "folha": {
                                        "dx": "Eritema multiforme",
                                        "justificativa": [
                                            "Lesões eritemato-descamativas, secas e esfoliativas disseminadas pelo corpo do paciente são clássicas da eritrodermia esfoliativa."
                                        ],
                                        "orientacoes": [
                                            "A maioria dos episódios de EM resolve espontaneamente em poucas semanas.",
                                            "No caso das lesões de EM provocarem sintomas com impacto negativo na qualidade de vida, é necessário tratamento de alívio sintomático.",
                                            "Poderá ser administrado anti-histamínico para alívio de prurido, corticoides tópicos cutâneos, gel bucal para diminuir a inflamação e acelerar o processo de cicatrização das lesões, elixires bucais com mistura de lidocaína e difenidramina que funcionam como antissépticos para dificultar a penetração de agentes patogênicos nas lesões mucosas e, por outro lado, diminuir a dor"
                                        ]
                                    }
                                },
                                # NÃO lesões em alvo --> diagnóstico inconclusivo
                                "2": {
                                    "folha": {
                                        "dx": "Diagnóstico inconclusivo",
                                        "justificativa": [
                                            "A descrição das lesões não se encaixa na literatura dermatológica.",
                                            "Lesões eritemato-descamativas disseminadas são secas e esfoliativas ou apresentam-se em alvo."
                                        ],
                                        "orientacoes": [
                                            "Reavalie as informações, pois se as lesões eritemato-descamativas estão disseminadas, mas não são secas e esfoliativas e nem se apresentam em alvo, deve haver algum equívoco."
                                        ]
                                    }
                                }
                            }
                        }
                    }
                },

                # NÃO espalhadas --> investigar dermatites (DA, DC, DS)
                "2": {
                    "caracteristica": "tipo_pele_dermatite_oleosa",
                    "pergunta": "O(a) paciente apresenta pele oleosa?",
                    "ramos": {
                        # SIM pele oleosa --> sugere DS ou DC
                        "1": {
                            "caracteristica": "historico_dermatite_seborreica",
                            "pergunta": "Há histórico de estresse, caso familiar ou HIV?",
                            "ramos": {
                                # SIM histórico DS --> sugere DS
                                "1": {
                                    "caracteristica": "local_dermatite_seborreica",
                                    "pergunta": "As lesões se concentram no couro cabeludo, face ou tronco?",
                                    "ramos": {
                                        # SIM local DS --> DS com certeza
                                        "1": {
                                            "folha": {
                                                "dx": "Dermatite seborreica",
                                                "justificativa": [
                                                    "Lesões eritemato-descamativas localizadas no couro cabeludo, face ou tronco em pacientes de pele oleosa com historico relevante para DS."
                                                ],
                                                "orientacoes": [
                                                    "Utilize shampoos com ácido salicílico e enxágue após alguns minutos.",
                                                    "Evite água muito quente e sabonetes irritantes.",
                                                    "Mantenha a pele hidratada com produtos suaves.",
                                                    "Em áreas do rosto ou corpo, use cremes de hidrocortisona (corticosteroides suaves) e, em casos mais persistentes, produtos com cetoconazol ou inibidores de calcineurina.",
                                                    "Controlar o estresse também ajuda a reduzir as crises"
                                                ]
                                            }
                                        },
                                        # NÃO local DS --> sugere DS
                                        "2": {
                                            "folha": {
                                                "dx": "Dermatite seborreica - possível",
                                                "justificativa": [
                                                    "Lesões eritemato-descamativas em pacientes de pele oleosa com historico relevante para DS.",
                                                    "Reavalie as regiões afetadas pelas lesões, pois todas as outras informações sugerem DS."
                                                ],
                                                "orientacoes": [
                                                    "Utilize shampoos com ácido salicílico e enxágue após alguns minutos.",
                                                    "Evite água muito quente e sabonetes irritantes.",
                                                    "Mantenha a pele hidratada com produtos suaves.",
                                                    "Em áreas do rosto ou corpo, use cremes de hidrocortisona (corticosteroides suaves) e, em casos mais persistentes, produtos com cetoconazol ou inibidores de calcineurina.",
                                                    "Controlar o estresse também ajuda a reduzir as crises"
                                                ]
                                            }
                                        }
                                    }
                                },

                                # NÃO histórico DS --> pele oleosa --> sugere DC
                                "2": {
                                    "caracteristica": "historico_dermatite_contato",
                                    "pergunta": "Houve manuseio de algum produto irritante?",
                                    "ramos": {
                                        # SIM historico DC --> pele oleosa - histórico DS + historico DC --> sugere DC
                                        "1": {
                                            "caracteristica": "local_dermatite_contato",
                                            "pergunta": "As lesões se localizam próximas ou nas áreas de contato com o produto irritante?",
                                            "ramos": {
                                                # SIM local DC --> pele oleosa - histórico DS + histórico DC + local DC --> DC !!!
                                                "1": {
                                                    "folha": {
                                                        "dx": "Dermatite de contato",
                                                        "justificativa": [
                                                            "Lesões eritemato-descamativas em pacientes de pele oleosa com historico relevante para DC."
                                                        ],
                                                        "orientacoes": [
                                                            "Evitar o agente causador.",
                                                            "Compressas frias, compressas úmidas, cremes com corticosteroides (sob orientação médica) e hidratação da pele",
                                                            "Evite coçar"
                                                        ]
                                                    }
                                                },
                                                # NÃO local DC --> pele oleosa - historico DS - historico DC - local DC --> perguntar local DS
                                                "2": {
                                                    "caracteristica": "local_dermatite_seborreica",
                                                    "pergunta": "As lesões se concentram no couro cabeludo, face ou tronco?",
                                                    "ramos": {
                                                        # SIM local DS --> pele oleosa - historico DS - historico DC - local DC + local DS --> sugere DS
                                                        "1": {
                                                            "folha": {
                                                                "dx": "Dermatite seborreica - possível",
                                                                "justificativa": [
                                                                    "Lesões eritemato-descamativas localizadas no couro cabeludo, face ou tronco em pacientes de pele oleosa.",
                                                                    "Reavalie o histórico do paciente, pois todas as outras informações descartam DC e sugerem DS."
                                                                ],
                                                                "orientacoes": [
                                                                    "Utilize shampoos com ácido salicílico e enxágue após alguns minutos.",
                                                                    "Evite água muito quente e sabonetes irritantes.",
                                                                    "Mantenha a pele hidratada com produtos suaves.",
                                                                    "Em áreas do rosto ou corpo, use cremes de hidrocortisona (corticosteroides suaves) e, em casos mais persistentes, produtos com cetoconazol ou inibidores de calcineurina.",
                                                                    "Controlar o estresse também ajuda a reduzir as crises"
                                                                ]
                                                            }
                                                        },
                                                        # NÃO local DS --> pele oleosa - historico DS - historico DC - local DC - local DS --> inconclusivo
                                                        "2": {
                                                            "folha": {
                                                                "dx": "Dermatite (DC ou DS) - investigar; diagnóstico ainda inconclusivo",
                                                                "justificativa": [
                                                                    "Lesões eritemato-descamativas em pacientes de pele oleosa sugerem DC ou DS.",
                                                                    "Porém, os históricos e localizaçãoes não condizem com as doenças. Talvez a pele do paciente não seja oleosa..."
                                                                ],
                                                                "orientacoes": [
                                                                    "Reavalie o(a) paciente, especialmente com relação ao tipo de pele dele(a)."
                                                                ]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        },
                                        # NÃO local DS --> SIM pele oleosa - NÃO histórico + SIM local --> sugere DS
                                        "2": {
                                            "folha": {
                                                "dx": "Dermatite seborreica - investigar",
                                                "justificativa": [
                                                    "Lesões eritemato-descamativas em pacientes de pele oleosa sugerem DS.",
                                                    "Reavalie as regiões afetadas pelas lesões e se há histórico de estresse, caso familiar o estresse, pois as outras informações sugerem DS."
                                                ],
                                                "orientacoes": [
                                                    "Utilize shampoos com ácido salicílico e enxágue após alguns minutos.",
                                                    "Evite água muito quente e sabonetes irritantes.",
                                                    "Mantenha a pele hidratada com produtos suaves.",
                                                    "Em áreas do rosto ou corpo, use cremes de hidrocortisona (corticosteroides suaves) e, em casos mais persistentes, produtos com cetoconazol ou inibidores de calcineurina.",
                                                    "Controlar o estresse também ajuda a reduzir as crises"
                                                ]
                                            }
                                        }
                                    }
                                }
                            }
                        },

                        # NÃO pele oleosa --> NÃO espalhada --> saber se a pele é seca
                        "2": {
                            "caracteristica": "tipo_pele_dermatite_seca",
                            "pergunta": "A pele do(a) paciente é seca/ressecada?",
                            "ramos": {
                                # SIM pele seca --> NÃO espalhada + pele seca --> sugere DA ou DC
                                "1": {
                                    "caracteristica": "historico_dermatite_atopica",
                                    "pergunta": "Há histórico de atopia (asma/rinite)?",
                                    "ramos": {
                                        # SIM histórico DA --> NÃO espalhada + pele seca + histórico DA --> DA
                                        "1": {
                                            "folha": {
                                                "dx": "Dermatite atópica",
                                                "justificativa": [
                                                    "Lesões eritemato-descamativas em pacientes de pele seca com historico relevante para DA.",
                                                ],
                                                "orientacoes": [
                                                    "Mantenha a pele hidratada com cremes adequados",
                                                    "Evite banhos quentes e longos, e use sabonetes neutros e líquidos.",
                                                    "Vista roupas de algodão e evite tecidos sintéticos, e use roupas leves e largas.",
                                                    "Identifique e evite gatilhos como alérgenos (ácaros, pelos de animais) e irritantes (perfumes, detergentes)"
                                                ]
                                            }
                                        },
                                        # NÃO histórico DA --> NÃO espalhada + pele seca - histórico DA --> perguntar histórico DC
                                        "2": {
                                            "caracteristica": "historico_dermatite_contato",
                                            "pergunta": "Houve manuseio de algum produto irritante?",
                                            "ramos": {
                                                # SIM histórico DC --> NÃO espalhada + pele seca - histórico DA + histórico DC --> DC
                                                "1": {
                                                    "folha": {
                                                        "dx": "Dermatite de contato",
                                                        "justificativa": [
                                                            "Lesões eritemato-descamativas em pacientes de pele seca com historico relevante para DC."
                                                        ],
                                                        "orientacoes": [
                                                            "Evitar o agente causador.",
                                                            "Compressas frias, compressas úmidas, cremes com corticosteroides (sob orientação médica) e hidratação da pele",
                                                            "Evite coçar"
                                                        ]
                                                    }
                                                },
                                                # NÃO histórico DC --> NÃO espalhada + pele seca - histórico DA - histórico DC --> inconclusivo
                                                "2": {
                                                    "folha": {
                                                        "dx": "Dermatite (DA ou DC) - investigar; diagnóstico ainda inconclusivo",
                                                        "justificativa": [
                                                            "Lesões eritemato-descamativas em pacientes de pele seca indicam DA ou DC.",
                                                            "Porém, os históricos não são relevantes para essas doenças."
                                                        ],
                                                        "orientacoes": [
                                                            "Reavalie o(a) paciente e solicite uma biópsia."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },

                                # NÃO oleosa, NÃO seca, NÃO espalhada --> perguntar sintomas DC
                                "2": {
                                    "caracteristica": "sintoma_dermatite_contato",
                                    "pergunta": "O(a) paciente relata sensação de ardor/queimação nas lesões?",
                                    "ramos": {
                                        # SIM sintoma DC --> sugere DC
                                        "1": {
                                            "caracteristica": "historico_dermatite_contato",
                                            "pergunta": "Houve manuseio de algum produto irritante?",
                                            "ramos": {
                                                # SIM historico DC --> NÃO espalhada + histórico DC --> sugere DC
                                                "1": {
                                                    "folha": {
                                                        "dx": "Dermatite de contato - possível",
                                                        "justificativa": [
                                                            "Lesões eritemato-descamativas não disseminadas envolvendo contato com produtos irriteantes sugerem DC."
                                                        ],
                                                        "orientacoes": [
                                                             "Evitar o agente causador.",
                                                            "Compressas frias, compressas úmidas, cremes com corticosteroides (sob orientação médica) e hidratação da pele",
                                                            "Evite coçar"
                                                        ]
                                                    }
                                                },
                                                # NÃO histórico DC --> inconclusivo
                                                "2": {
                                                    "folha": {
                                                        "dx": "Dermatite - investigar; diagnóstico ainda inconclusivo",
                                                        "justificativa": [
                                                            "Lesões eritemato-descamativas não disseminadas indicam dermatites",
                                                            "Porém, não há informações suficientes para classificar o tipo de dermatite."
                                                        ],
                                                        "orientacoes": [
                                                            "Reavalie o(a) paciente e solicite uma biópsia."
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        # NÃO sintomas DC --> inconclusivo
                                        "2": {
                                            "folha": {
                                                "dx": "Dermatite - investigar; diagnóstico ainda inconclusivo",
                                                "justificativa": [
                                                    "Lesões eritemato-descamativas não disseminadas indicam dermatites",
                                                    "Porém, não há informações suficientes para classificar o tipo de dermatite."
                                                ],
                                                "orientacoes": [
                                                    "Reavalie o(a) paciente e solicite uma biópsia."
                                                ]
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        },
        
        "C": {
            "caracteristica": "lesoes_vesiculares_disseminadas",
            "pergunta": "As lesões vesiculares estão espalhadas pelo corpo do(a) paciente?",
            "ramos": {
                "1": {  # SIM: vesículas disseminadas
                    "caracteristica": "sintomas_sistemicos_varicela",
                    "pergunta": "O(a) paciente apresenta febre, mal-estar, cansaço, dor de cabeça ou perda de apetite?",
                    "ramos": {
                        "1": {  # SIM: possui sintomas sistêmicos
                            "caracteristica": "prurido_local",
                            "pergunta": "Há prurido (coceira) no local das lesões?",
                            "ramos": {
                                "1": {  # SIM prurido
                                    "caracteristica": "eh_crianca",
                                    "pergunta": "O(a) paciente é criança?",
                                    "ramos": {
                                        "1": {  # criança
                                            "folha": {
                                                "dx": "Varicela (catapora)",
                                                "justificativa": [
                                                    "Vesículas disseminadas + sintomas sistêmicos + prurido em criança"
                                                ],
                                                "orientacoes": [
                                                    "Suporte, anti-pruriginosos; avaliar vacina/contatos; sinais de gravidade."
                                                ]
                                            }
                                        },
                                        "2": {  # não é criança
                                            "folha": {
                                                "dx": "Varicela — provável",
                                                "justificativa": [
                                                    "Vesículas disseminadas + sintomas sistêmicos + prurido em não-criança"
                                                ],
                                                "orientacoes": [
                                                    "Suporte, anti-pruriginosos; avaliar terapia antiviral conforme caso."
                                                ]
                                            }
                                        }
                                    }
                                },
                                "2": {  # NÃO prurido
                                    "caracteristica": "eh_crianca",
                                    "pergunta": "O(a) paciente é criança?",
                                    "ramos": {
                                        "1": {  # criança
                                            "caracteristica": "manchas_avermelhadas_disseminadas",
                                            "pergunta": "Há manchas avermelhadas pelo corpo todo?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Varicela — possível",
                                                        "justificativa": [
                                                            "Vesículas disseminadas + sintomas sistêmicos em criança + exantema"
                                                        ],
                                                        "orientacoes": [
                                                            "Conduta de suporte; observar evolução; retorno se piora."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Varicela — provável",
                                                        "justificativa": [
                                                            "Vesículas disseminadas + sintomas sistêmicos em criança"
                                                        ],
                                                        "orientacoes": [
                                                            "Conduta de suporte; considerar avaliação pediátrica."
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        "2": {  # não é criança
                                            "caracteristica": "manchas_avermelhadas_disseminadas",
                                            "pergunta": "Há manchas avermelhadas pelo corpo todo?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Varicela — investigar",
                                                        "justificativa": [
                                                            "Vesículas disseminadas + sintomas sistêmicos em adulto + exantema"
                                                        ],
                                                        "orientacoes": [
                                                            "Considerar exames, gravidade, condições de risco e antiviral."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Diagnóstico inconclusivo",
                                                        "justificativa": [
                                                            "Vesículas disseminadas com sintomas sistêmicos, sem outros marcadores"
                                                        ],
                                                        "orientacoes": [
                                                            "Reavaliar; considerar exames e diagnóstico diferencial."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "2": {  # NÃO tem sintomas sistêmicos
                            "caracteristica": "prurido_local",
                            "pergunta": "Há prurido (coceira) no local das lesões?",
                            "ramos": {
                                "1": {  # SIM prurido
                                    "caracteristica": "eh_crianca",
                                    "pergunta": "O(a) paciente é criança?",
                                    "ramos": {
                                        "1": {
                                            "folha": {
                                                "dx": "Varicela — possível",
                                                "justificativa": [
                                                    "Vesículas disseminadas com prurido em criança (sintomas sistêmicos ausentes)"
                                                ],
                                                "orientacoes": [
                                                    "Conduta de suporte e observação; retorno se surgirem sintomas sistêmicos."
                                                ]
                                            }
                                        },
                                        "2": {
                                            "folha": {
                                                "dx": "Varicela — provável",
                                                "justificativa": [
                                                    "Vesículas disseminadas com prurido em não-criança"
                                                ],
                                                "orientacoes": [
                                                    "Considerar antiviral conforme risco; reavaliar evolução."
                                                ]
                                            }
                                        }
                                    }
                                },
                                "2": {  # NÃO prurido
                                    "caracteristica": "eh_crianca",
                                    "pergunta": "O(a) paciente é criança?",
                                    "ramos": {
                                        "1": {
                                            "caracteristica": "manchas_avermelhadas_disseminadas",
                                            "pergunta": "Há manchas avermelhadas pelo corpo todo?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Varicela — possível",
                                                        "justificativa": [
                                                            "Vesículas disseminadas em criança com exantema, sem sintomas sistêmicos"
                                                        ],
                                                        "orientacoes": [
                                                            "Suporte e observação; alertar sinais de gravidade."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Varicela — provável",
                                                        "justificativa": [
                                                            "Vesículas disseminadas em criança, sem sintomas sistêmicos"
                                                        ],
                                                        "orientacoes": [
                                                            "Suporte; reavaliação clínica conforme evolução."
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        "2": {
                                            "caracteristica": "manchas_avermelhadas_disseminadas",
                                            "pergunta": "Há manchas avermelhadas pelo corpo todo?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Varicela — investigar",
                                                        "justificativa": [
                                                            "Vesículas disseminadas em adulto + exantema, sem sintomas sistêmicos"
                                                        ],
                                                        "orientacoes": [
                                                            "Investigar; considerar antiviral conforme risco."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Diagnóstico inconclusivo",
                                                        "justificativa": [
                                                            "Vesículas disseminadas sem sintomas e sem exantema difuso"
                                                        ],
                                                        "orientacoes": [
                                                            "Reavaliar; considerar outros diagnósticos diferenciais."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                },
                "2": {  # NÃO: não estão disseminadas → herpes/zóster
                    "caracteristica": "ardor_ou_prurido_lesoes",
                    "pergunta": "O(a) paciente apresenta ardor e/ou prurido no local das lesões?",
                    "ramos": {
                        "1": {  # SIM ardor/prurido
                            "caracteristica": "eh_adulto",
                            "pergunta": "O(a) paciente é adulto?",
                            "ramos": {
                                "1": {  # adulto
                                    "caracteristica": "local_genitais",
                                    "pergunta": "As lesões estão localizadas nos genitais?",
                                    "ramos": {
                                        "1": {
                                            "folha": {
                                                "dx": "Herpes simples tipo 1 > tipo 2 (genitais)",
                                                "justificativa": [
                                                    "Vesículas/ulcerações dolorosas pruriginosas em genitais (adulto)"
                                                ],
                                                "orientacoes": [
                                                    "Antiviral conforme protocolo; orientação sexual e prevenção."
                                                ]
                                            }
                                        },
                                        "2": {
                                            "caracteristica": "local_boca",
                                            "pergunta": "As lesões estão localizadas na boca?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Herpes simples tipo 2 > tipo 1 (oral)",
                                                        "justificativa": [
                                                            "Vesículas/ulcerações com ardor/prurido em cavidade oral (adulto)"
                                                        ],
                                                        "orientacoes": [
                                                            "Antiviral tópico/sistêmico conforme gravidade."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Herpes simples (adulto)",
                                                        "justificativa": [
                                                            "Vesículas/ulcerações localizadas com ardor/prurido (adulto)"
                                                        ],
                                                        "orientacoes": [
                                                            "Antiviral conforme caso; educação em recorrência."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "2": {  # não é adulto → perguntar criança
                                    "caracteristica": "eh_crianca",
                                    "pergunta": "O(a) paciente é criança?",
                                    "ramos": {
                                        "1": {
                                            "caracteristica": "local_boca",
                                            "pergunta": "As lesões estão localizadas na boca?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Herpes simples (infantil)",
                                                        "justificativa": [
                                                            "Vesículas/ulcerações orais com ardor/prurido em criança"
                                                        ],
                                                        "orientacoes": [
                                                            "Suporte; considerar antiviral conforme gravidade."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Herpes simples — provável (infantil)",
                                                        "justificativa": [
                                                            "Vesículas localizadas com ardor/prurido em criança"
                                                        ],
                                                        "orientacoes": [
                                                            "Observação e suporte; retorno se piora."
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        "2": {
                                            "caracteristica": "historico_catapora_ou_imunossup",
                                            "pergunta": "O(a) paciente já teve catapora e/ou apresenta imunossupressão?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Herpes zóster",
                                                        "justificativa": [
                                                            "Reativação pós-varicela ou imunossupressão com dor/vesículas em dermátomo"
                                                        ],
                                                        "orientacoes": [
                                                            "Antiviral precoce; analgesia; avaliar extensão/complicações."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "caracteristica": "local_boca",
                                                    "pergunta": "As lesões estão localizadas na boca?",
                                                    "ramos": {
                                                        "1": {
                                                            "folha": {
                                                                "dx": "Herpes simples",
                                                                "justificativa": [
                                                                    "Vesículas/ulcerações orais localizadas"
                                                                ],
                                                                "orientacoes": [
                                                                    "Antiviral tópico/sistêmico conforme gravidade."
                                                                ]
                                                            }
                                                        },
                                                        "2": {
                                                            "folha": {
                                                                "dx": "Herpes simples — provável",
                                                                "justificativa": [
                                                                    "Lesões vesiculoulceradas localizadas sem fatores adicionais"
                                                                ],
                                                                "orientacoes": [
                                                                    "Acompanhamento; orientar sinais de alarme."
                                                                ]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "2": {  # NÃO ardor/prurido
                            "caracteristica": "eh_adulto",
                            "pergunta": "O(a) paciente é adulto?",
                            "ramos": {
                                "1": {  # adulto
                                    "caracteristica": "local_genitais",
                                    "pergunta": "As lesões estão localizadas nos genitais?",
                                    "ramos": {
                                        "1": {
                                            "folha": {
                                                "dx": "Herpes simples tipo 1 > tipo 2 (genitais)",
                                                "justificativa": [
                                                    "Vesículas/ulcerações genitais localizadas (adulto)"
                                                ],
                                                "orientacoes": [
                                                    "Antiviral conforme protocolo; aconselhamento."
                                                ]
                                            }
                                        },
                                        "2": {
                                            "caracteristica": "local_boca",
                                            "pergunta": "As lesões estão localizadas na boca?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Herpes simples tipo 2 > tipo 1 (oral)",
                                                        "justificativa": [
                                                            "Vesículas/ulcerações orais localizadas (adulto)"
                                                        ],
                                                        "orientacoes": [
                                                            "Antiviral; suporte sintomático."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Herpes simples (adulto)",
                                                        "justificativa": [
                                                            "Lesões vesiculoulceradas localizadas (adulto)"
                                                        ],
                                                        "orientacoes": [
                                                            "Conduta conforme gravidade/recorrência."
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    }
                                },
                                "2": {  # não é adulto → perguntar criança
                                    "caracteristica": "eh_crianca",
                                    "pergunta": "O(a) paciente é criança?",
                                    "ramos": {
                                        "1": {
                                            "caracteristica": "local_boca",
                                            "pergunta": "As lesões estão localizadas na boca?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Herpes simples (infantil)",
                                                        "justificativa": [
                                                            "Lesões vesiculoulceradas orais localizadas em criança"
                                                        ],
                                                        "orientacoes": [
                                                            "Suporte/antiviral conforme caso."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "folha": {
                                                        "dx": "Herpes simples — provável (infantil)",
                                                        "justificativa": [
                                                            "Lesões vesiculoulceradas localizadas em criança"
                                                        ],
                                                        "orientacoes": [
                                                            "Observação e retorno se piora."
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        "2": {
                                            "caracteristica": "historico_catapora_ou_imunossup",
                                            "pergunta": "O(a) paciente já teve catapora e/ou apresenta imunossupressão?",
                                            "ramos": {
                                                "1": {
                                                    "folha": {
                                                        "dx": "Herpes zóster",
                                                        "justificativa": [
                                                            "Fator predisponente (pós-varicela/imunossupressão) + topografia típica"
                                                        ],
                                                        "orientacoes": [
                                                            "Antiviral; analgesia; avaliar neuralgia pós-herpética."
                                                        ]
                                                    }
                                                },
                                                "2": {
                                                    "caracteristica": "local_boca",
                                                    "pergunta": "As lesões estão localizadas na boca?",
                                                    "ramos": {
                                                        "1": {
                                                            "folha": {
                                                                "dx": "Herpes simples",
                                                                "justificativa": [
                                                                    "Lesões orais localizadas compatíveis com herpes"
                                                                ],
                                                                "orientacoes": [
                                                                    "Antiviral conforme protocolo."
                                                                ]
                                                            }
                                                        },
                                                        "2": {
                                                            "folha": {
                                                                "dx": "Herpes simples — provável",
                                                                "justificativa": [
                                                                    "Quadro compatível sem marcadores adicionais"
                                                                ],
                                                                "orientacoes": [
                                                                    "Acompanhamento clínico; orientar retorno."
                                                                ]
                                                            }
                                                        }
                                                    }
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }  
}
