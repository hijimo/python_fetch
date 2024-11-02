
const createIngredientModel = (db) => {

    const Ingredient = db.define("t_ingredient", {
        id: {type:'serial', key:true},
        calory: {type:'number', },
        joule: {type:'number', },
        gi: {type:'number', },
        gl: {type:'number', },
        protein: {type:'number', },
        fat: {type:'number', },
        saturated_fat: {type:'number', },
        fatty_acid: {type:'number', },
        mufa: {type:'number', },
        pufa: {type:'number', },
        carbohydrate: {type:'number', },
        fiber_dietary: {type:'number', },
       
        cholesterol: {type:'number', },
        sugar: {type:'number', },
        alcohol: {type:'number', },
        
       
// 重金属
        magnesium: {type:'number', },
        calcium: {type:'number', },
        iron: {type:'number', },
        zinc: {type:'number', },
        copper: {type:'number', },
        manganese: {type:'number', },
        kalium: {type:'number', },
        phosphor: {type:'number', },
        natrium: {type:'number', },
        fluorine: {type:'number', },
        iodine: {type:'number', },
        selenium: {type:'number', },
    //    唯生素
        vitamin_a: {type:'number', },
        carotene: {type:'number', },
        thiamine: {type:'number', },
        lactoflavin: {type:'number', },
        vitamin_b6: {type:'number', },
        vitamin_b12: {type:'number', },
        vitamin_c: {type:'number', },
        vitamin_d: {type:'number', },
        vitamin_e: {type:'number', },
        vitamin_k: {type:'number', },
        niacin: {type:'number', },
        folacin: {type:'number', },
        pantothenic: {type:'number', },
        biotin: {type:'number', },
        choline: {type:'number', },
       
        

    }, {
        methods: {

        },
        validations: {
        }
    });
    return Ingredient;
}

module.exports = createIngredientModel


