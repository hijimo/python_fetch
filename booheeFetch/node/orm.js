const orm = require('orm')

orm.connect("mysql://username:password@host/database", function (err, db) {
  if (err) throw err;
 
 
  // add the table to the database
  db.sync(function(err) {
    if (err) throw err;
 
    // add a row to the person table
    // Person.create({ id: 1, name: "John", surname: "Doe", age: 27 }, function(err) {
    //   if (err) throw err;
 
    // });
  });
});
