
const orm = require('orm')
const createFoodModel = require('./models/food') 
const createIngredientModel = require('./models/ingredient') 

// food 是v2接口
// food_old是旧接口，两个接口返回数据不一样。
const insert = (db,food, cb) => {
 // add the table to the database
 db.sync(function(err) {
  if (err) throw err;
// 添加食物主表
  const Food = createFoodModel(db);
  Food.create({
      id: food.id,
      name: food['basic_section'].name,
      code: food.code,
      brand: null,
      weight: null,
      health_light:food['basic_section']['health_light'],
      liquid: null,
      thumb: food['basic_section']['thumb_image_url'],
      large: food['basic_section']['large_image_url'],
      appraise: null,
      ingredient_id:food.id,
      category:  food['calory_section']['ranking']['name'],
      calory_rank: food['calory_section']['ranking']['calory_rank'],
      rank_id: food['calory_section']['ranking']['id']
  }, function(err){
      if (err) throw err;
      console.log(`添加食物:${food['basic_section'].name}成功，id为:${food.id}`)
  })
  // 添加营养成分表
  const Ingredient = createIngredientModel(db);
  Ingredient.create({
    id: food.id,
    calory: food["ingredient_section"]["main_ingredient"]["calory"]|| null,
    joule: food["calory_section"]["joule"]|| null,
    gi: food["glycemic_section"]["gi"]["value"]|| null,
    gl: food["glycemic_section"]["gl"]["value"]|| null,
    protein: food["ingredient_section"]["main_ingredient"]["protein"]|| null,
    fat: food["ingredient_section"]["main_ingredient"]["fat"]|| null,
    saturated_fat: food["ingredient_section"]["main_ingredient"]["saturated_fat"]|| null,
    fatty_acid: food["ingredient_section"]["main_ingredient"]["fatty_acid"] || null,
    mufa: food["ingredient_section"]["main_ingredient"]["mufa"]|| null,
    pufa: food["ingredient_section"]["main_ingredient"]["pufa"]|| null,
    carbohydrate: food["ingredient_section"]["main_ingredient"]["carbohydrate"]|| null,
    fiber_dietary: food["ingredient_section"]["main_ingredient"]["fiber_dietary"]|| null,
    cholesterol: food["ingredient_section"]["main_ingredient"]["cholesterol"]|| null,
    sugar: food["ingredient_section"]["main_ingredient"]["sugar"]|| null,
    natrium: food["ingredient_section"]["main_ingredient"]["natrium"]|| null,
    alcohol: food["ingredient_section"]["main_ingredient"]["alcohol"]|| null,
    
    
    
   
// 矿物质
    magnesium: food["ingredient_section"]["minerals_ingredient"]["magnesium"]|| null,
    calcium: food["ingredient_section"]["minerals_ingredient"]["calcium"]|| null,
    iron: food["ingredient_section"]["minerals_ingredient"]["iron"]|| null,
    zinc:food["ingredient_section"]["minerals_ingredient"]["zinc"]|| null,
    copper: food["ingredient_section"]["minerals_ingredient"]["copper"]|| null,
    manganese: food["ingredient_section"]["minerals_ingredient"]["manganese"]|| null,
    kalium: food["ingredient_section"]["minerals_ingredient"]["kalium"]|| null,
    phosphor: food["ingredient_section"]["minerals_ingredient"]["phosphor"]|| null,
    
    fluorine:food["ingredient_section"]["minerals_ingredient"]["fluorine"] || null,
    iodine: food["ingredient_section"]["minerals_ingredient"]["iodine"]|| null,
    selenium: food["ingredient_section"]["minerals_ingredient"]["selenium"]|| null,
//    唯生素
    vitamin_a: food["ingredient_section"]["vitamin_ingredient"]["vitamin_a"]|| null,
    carotene: food["ingredient_section"]["vitamin_ingredient"]["carotene"]|| null,
    thiamine: food["ingredient_section"]["vitamin_ingredient"]["thiamine"]|| null,
    lactoflavin:food["ingredient_section"]["vitamin_ingredient"]["lactoflavin"]|| null,
    vitamin_b6: food["ingredient_section"]["vitamin_ingredient"]["vitamin_b6"]|| null,
    vitamin_b12: food["ingredient_section"]["vitamin_ingredient"]["vitamin_b12"]|| null,
    vitamin_c: food["ingredient_section"]["vitamin_ingredient"]["vitamin_c"]|| null,
    vitamin_d:food["ingredient_section"]["vitamin_ingredient"]["vitamin_d"]|| null,
    vitamin_e:food["ingredient_section"]["vitamin_ingredient"]["vitamin_e"]|| null,
    vitamin_k:food["ingredient_section"]["vitamin_ingredient"]["vitamin_k"]|| null,
    niacin:food["ingredient_section"]["vitamin_ingredient"]["niacin"]|| null,
    folacin:food["ingredient_section"]["vitamin_ingredient"]["folacin"]|| null,
    pantothenic:food["ingredient_section"]["vitamin_ingredient"]["pantothenic"]|| null,
    biotin: food["ingredient_section"]["vitamin_ingredient"]["biotin"]|| null,
    choline:food["ingredient_section"]["vitamin_ingredient"]["choline"]|| null,
  }, function(err){
      if (err) throw err;
      console.log(`添加食物:${food['basic_section'].name}营养副表成功，id为:${food.id}`);
      cb && cb()
  })
});
}


 const connect = (cb) => {
  orm.connect("mysql://root_shangqi:RUhSdnZ*lDh\@@rm-bp1h6486n1s9oc261jo.mysql.rds.aliyuncs.com:3306/db_foods", function (err, db) {
    if (err) throw err;

    cb && cb(db)
     
     
     
    });
}

connect();


module.exports = {
  insert,
  connect
}


