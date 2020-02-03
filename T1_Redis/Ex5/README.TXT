Para este exercício decidi utilizar 3 estuturas de dados (do redis):
	LIST - users:messages:<username> 
		Lista que contem todas as mensages postadas pelo user especificado em <username>
	
	LIST - users:subscriptions:<username>
		Lista que contem todos users a quem o <username> está subscripto

	HASH - users:info:<username>
		Hash que contem informação sobre o <username>. Estas consistem nos campos: name (username do <username>) ; password (password do <username>) ; posts (numero de posts efetuados pelo <username>) ; subscriptions (subscriçoes do <username>)
