const orm = require('orm')
const fs = require('fs')
const path = require('path')
const createFoodModel = require('./models/food') 

const logger = (msg)=> {
    const filename = path.join(__dirname,'log/log.log')
    console.log(msg )
    fs.writeFile(filename, `${new Date().valueOf()}: ${msg}`,{flag:'a',encoding:'utf-8', mode:'0644'},(err)=>{})
}
// 将旧的食物数据字段更新到数据库
 const uploadFields = (db, food, orginFields,targetFields,cb) => {
    db.sync(function(err) {
        if (err) throw err;
      // 添加食物主表
        const Food = createFoodModel(db);
       Food.find({id:food.id},(err,foodsByDb)=>{
           if(err) throw err;
           if(foodsByDb.length) {
            orginFields.forEach((key,idx)=>{
                if (food[key] !== null) {
                    foodsByDb[0][targetFields[idx]]=food[key]
                }
                
            })
            foodsByDb[0].save((err)=>{
                if(err) {
                    throw err;
                }
                console.log('update food name:',food.name,' food id:',food.id,' success')
                cb && cb()
                
            })
           } else {
               
               logger(`food name ${food.name}, food id ${food.id} 不存在` )

               cb && cb()
           }
           
       })
      });
}

module.exports = {
    uploadFields
}