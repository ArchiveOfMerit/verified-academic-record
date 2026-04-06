const dissentStatement = {
  author: "Justin Ames Gamache",
  action: "dissents against",
  subject: "Vermont"
};

function getDissentText(statement) {
  return `${statement.author} ${statement.action} ${statement.subject}.`;
}

console.log(getDissentText(dissentStatement));
