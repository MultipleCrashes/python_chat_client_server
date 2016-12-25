var MongoClient = require('mongodb').MongoClient


MongoClient.connect('mongodb://localhost:27017/whatsapp',function(err,db){
		var collection = db.collection('chat')
		var stream = collection.find().stream();
	       	stream.on('data',function(data){
			console.log(data);
		});
   });

