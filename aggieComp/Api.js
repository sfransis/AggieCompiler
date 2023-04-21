


const express = require("express")
const app = express()
const bodyP = require("body-parser")
const compiler = require("compilex")
const options = {stats: true}

compiler.init(options)
app.use(bodyP.json())

app.use("/aggieComp", express.static("/Users/kharo019/Documents/CS/CS448/Github-AggieCompiler/AggieCompiler/aggieComp"))
app.get("/", function(req,res){
	res.sendFile("/Users/kharo019/Documents/CS/CS448/Github-AggieCompiler/AggieCompiler/aggieComp/templates/compiler.html")
})
app.post("/aggieComp", functions(req, res){
	var code = req.body.code
	var input = req.body.input
	var lang = req.body.lang
	//if windows  
	var envData = { OS : "windows"}; 
	//else
	var envData = { OS : "linux" }; 
	compiler.compilePython( envData , code , function(data){
		res.send(data);
	});    

})

app.listen(8000)