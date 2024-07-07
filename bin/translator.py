raw_map="""²|Ա,´|Բ,¶|Գ,¸|Դ,º|Ե,¼|Զ,¾|Է,À|Ը,Â|Թ,Ä|Ժ,Æ|Ի,È|Լ,Ê|Խ,Ì|Ծ,Î|Կ,Ð|Հ,Ò|Ձ,Ô|Ղ,Ö|Ճ,Ø|Մ,Ú|Յ,Ü|Ն,Þ|Շ,à|Ո,â|Չ,ä|Պ,æ|Ջ,è|Ռ,ê|Ս,ì|Վ,î|Տ,ð|Ր,ò|Ց,ô|Ւ,ö|Փ,ø|Ք,ú|Օ,ü|Ֆ, | ,¡|©,¢|§,¤|),¥|(,¦|»,§|«,©|.,«|,,¬|-,®|…,þ|՚,ÿ|՚,°|՛,¯|՜,ª|՝,±|՞,³|ա,µ|բ,·|գ,¹|դ,»|ե,½|զ,¿|է,Á|ը,Ã|թ,Å|ժ,Ç|ի,É|լ,Ë|խ,Í|ծ,Ï|կ,Ñ|հ,Ó|ձ,Õ|ղ,×|ճ,Ù|մ,Û|յ,Ý|ն,ß|շ,á|ո,ã|չ,å|պ,ç|ջ,é|ռ,ë|ս,í|վ,ï|տ,ñ|ր,ó|ց,õ|ւ,÷|փ,ù|ք,û|օ,ý|ֆ,¨|և,£|։,ˊ|՛,́|́,ʹ|ʹ,†|†,μ|բ"""

def translate(original_str):

    map=raw_map.split(',')
    map_dict=dict(zip([entity.split('|')[0] for entity in map], [entity.split('|')[1] for entity in map]))

    trans_table = "".maketrans(map_dict)

    return original_str.translate(trans_table)
