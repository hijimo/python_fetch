
const createFoodModel = (db) => {

    const Food = db.define("t_foods", {
        id: {type:'serial', key:true},
        name: {type:'text', },
        code: {type:'text', },
        brand: {type:'text', },
        weight: {type:'text', },
        health_light: {type:'number', },
        liquid: {type:'boolean', },
        thumb: {type:'text', },
        large: {type:'text', },
        appraise: {type:'text', },
        ingredient_id: {type:'number', },
        category: {type:'text', },
        calory_rank: {type:'number', },
        rank_id: {type:'number', }

    }, {
        methods: {

        },
        validations: {
        }
    });
    return Food;
}
module.exports = createFoodModel

