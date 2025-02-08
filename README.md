Tüm rollerin olduğu 3 nodelu k8s cluster kurdum
Clustera storageclass olarak longhorn kurdum
Redis namespace'e oluşturup redis kurulumu yaptım
Redise bağlanan bir api yazdım. Bu apiye redisde key ekleyip silecek endpointler yazdım
Api clusterda her nodeda birer tane olacak şekilde deploy ettim ve ingress ile dışarıya açtım
Kurduğum redis'in volume'ü awsde bir s3 hesaba backupladım
Ve sildiğimde restore edilebilir olup olmadığını kontrol ettim. 

Bunu hem DigitalOcean'da hem de kendi ana bilgisayarımda yaptım.
