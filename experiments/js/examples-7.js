// examples chosen to correspond (at least loosely) with wordnet heirarchies
// Andrea Shulman (Summer 2017 RA, Stanford SymSys) helped in creating these

// examples stores the target sentences and an array of their corresponding context sentences
var examples = [{
	// warm and cold are not super context sensitive because of perception
	// the best example is of people from different places
	target: {
		positive: "warm",
		negative: "cold"
	},
	context: [
		" lives in Maryland and steps outside in Winter.",
		" lives in Maryland and steps outside in Fall.",
		" lives in Maryland and steps outside in Summer."
	],
	contextWithSuper: [
		" lives in Maryland and checks the weather everyday. They looks at the weather report for today, a day in Winter.",
		" lives in Maryland and checks the weather everyday. They looks at the weather report for today, a day in Fall.",
		" lives in Maryland and checks the weather everyday. They looks at the weather report for today, a day in Summer."
	],
	action: [
		" Imagine you live in Maryland and go outside on a day in Winter.",
		" Imagine you live in Maryland and go outside on a day in Fall.",
		" Imagine you live in Maryland and go outside on a day in Summer."
	],
	sub: {
		singular: [
			"day in Winter",
			"day in Fall",
			"day in Summer"
		],
		plural: [
			"days in Winter",
			"days in Fall",
			"days in Summer"
		]
	},
	super: "days of the year",
	strength: [1,2,3], // how high on the scale the sub-cat is expected to be
	degree: "temperature",
	unit: ["degrees Fahrenheit", "degrees Celsius"],
	subunit: ["none"]
},
{
	target: {
		positive: "warm",
		negative: "cold"
	},
	context: [
		" takes their first sip from a cup of iced tea.",
		" takes their first sip from a cup of water.",
		" takes their first sip from a cup of coffee."
	],
	// contextWithSuper: [
	// 	" drinks different beverages on different days. At the present moment, they takes a sip from a cup of iced tea.",
	// 	" drinks different beverages on different days. At the present moment, they takes a sip from a cup of water.",
	// 	" drinks different beverages on different days. At the present moment, they takes a sip from a cup of coffee."
	// ],
	action: [
		" Imagine taking a sip from a cup of iced tea.",
		" Imagine taking a sip from a cup of water.",
		" Imagine taking a sip from a cup of coffee.",
	],
	sub: {
		singular: [
			"cup of iced tea",
			"cup of water",
			"cup of coffee"
		],
		plural: [
			"cups of iced tea",
			"cups of water",
			"cups of coffee"
		]
	},
	super: "beverages",
	strength: [1,2,3], // how high on the scale the sub-cat is expected to be
	degree: "temperature",
	unit: ["degrees Fahrenheit", "degrees Celsius"],
	subunit: ["none"]
},
{
	target: {
		positive: "expensive",
		negative: "cheap"
	},
	context: [
		" looks at the price of a kids bike.",
		" looks at the price of a city bike.",
		" looks at the price of an electric bike."
	],
	// contextWithSuper: [
	// 	" is buying kitchen appliances for their new apartment. They find a coffee maker and looks at the price.",
	// 	" is buying kitchen appliances for their new apartment. They find a food processor and looks at the price.",
	// 	" is buying kitchen appliances for their new apartment. They find a stove and looks at the price."
	// ],
	action: [
		"Imagine you are buying a kids bike.",
		"Imagine you are buying a city bike.",
		"Imagine you are buying an electric bike."
	],
	sub: {
		singular: [
			"kids bike",
			"city bike",
			"electric bike"
		],
		plural: [
			"kids bikes",
			"city bikes",
			"electric bikes"
		]
	},
	super: "bikes",
	strength: [1,2,3],
	degree: "price",
	unit: ["dollars"],
	subunit: ["none"]
},
{ // This is cheap
	target: {
		positive: " expensive",
		negative: " cheap"
	},
	context: [
		" looks at the price of a flower vase made of plastic.",
		" looks at the price of a flower vase made of glass.",
		" looks at the price of a flower vase made of crystal."
	],
	contextWithSuper: [
		" is looking to buy a flower vase. They finds one made of plastic.",
		" is looking to buy a flower vase. They finds one made of glass.",
		" is looking to buy a flower vase. They finds one made of crystal.",
	],
	action: [
		"Imagine you are buying a flower vase made of plastic.",
		"Imagine you are buying a flower vase made of glass.",
		"Imagine you are buying a flower vase made of crystal."
	],
	sub: {
		singular: [
			"plastic flower vase",
			"glass flower vase",
			"crystal flower vase",
		],
		plural: [
			"plastic flower vases",
			"glass flower vases",
			"crystal flower vases",
		]
	},
	super: "flower vases",
	strength: [1,2,3],
	degree: "price",
	unit: ["dollars"],
	subunit: ["none"]
},
{
	target: {
		positive: "long",
		negative: "short"
	},
	context: [
		" is shown a flight from Los Angeles to San Francisco.",
		" is shown a driving route from Los Angeles to San Francisco.",
		" is shown a bike route from Los Angeles to San Francisco."
	],
	contextWithSuper: [
		" is searching for a way to get from Los Angeles to San Francisco. Their friend shows them a flight.",
		" is searching for a way to get from Los Angeles to San Francisco. Their friend shows them a driving route.",
		" is searching for a way to get from Los Angeles to San Francisco. Their friend shows them a bike route."
	],
	action: [
		"Imagine being shown a flight from Los Angeles to San Francisco.",
		"Imagine being shown a driving route from Los Angeles to San Francisco.",
		"Imagine being shown a bike route from Los Angeles to San Francisco.",
	],
	sub: {
		singular: [
			"flight from Los Angeles to San Francisco",
			"driving route from Los Angeles to San Francisco",
			"bike route from Los Angeles to San Francisco"
		],
		plural: [
			"flight froms Los Angeles to San Francisco",
			"driving routes from Los Angeles to San Francisco",
			"bike routes from Los Angeles to San Francisco"
		]
	},
	super: "ways of getting from Los Angeles to San Francisco",
	strength: [1,2,3],
	degree: "time",
	unit: ["seconds", "minutes", "hours", "days"],
	subunit: ["seconds", "minutes", "hours"]
},
{
	target: {
		positive: " tall",
		negative: " short"
	},
	context: [
		" sees a gymnast.",
		" sees a runner.",
		" sees a basketball player."
	],
	contextWithSuper: [
		" is sitting at a cafe watching people go by and sees a gymnast.",
		" is sitting at a cafe watching people go by and sees a runner.",
		" is sitting at a cafe watching people go by and sees a basketball player."
	],
	action: [
		"Imagine you see a gymnast.",
		"Imagine you see a runner.",
		"Imagine you see a basketball player."
	],
	sub: {
		singular: [
			"gymnast",
			"runner",
			"basketball player"
		],
		plural: [
			"gymnasts",
			"runners",
			"basketball players"
		]
	},
	super: "people",
	strength: [1,2,3],
	degree: "height",
	unit: ["feet", "meters"],
	subunit: ["inches", "centimeters"]
},
{
	target: {
		positive: "big",
		negative: "small"
	},
	context: [
		" sees a porcupine.",
		" sees a chimpanzee.",
		" sees an elephant."
	],
	contextWithSuper: [
		" is on a safari looking at animals and sees a porcupine.",
		" is on a safari looking at animals and sees a chimpanzee.",
		" is on a safari looking at animals and sees an elephant."
	],
	action: [
		"Imagine you see a porcupine.",
		"Imagine you see a chimpanzee.",
		"Imagine you see an elephant."
	],
	sub: {
		singular: [
			"porcupine",
			"chimpanzee",
			"elephant"
		],
		plural: [
			"porcupines",
			"chimpanzees",
			"elephants"
		],
	},
	super: "animals",
	strength: [1,2,3],
	degree: "height",
	unit: ["feet", "meters"],
	subunit: ["inches", "centimeters"]
},
{
	target: {
		positive: "big",
		negative: "small"
	},
	context: [
		" gets into a sports car.",
		" gets into a sedan.",
		" gets into an SUV."
	],
	contextWithSuper: [
		" is test driving cars and gets into a sports car.",
		" is test driving cars and gets into a sedan.",
		" is test driving cars and gets into an SUV.",
	],
	action: [
		"Imagine you get into a sports car.",
		"Imagine you get into a sedan.",
		"Imagine you get into an SUV.",
	],
	sub: {
		singular: [
			"sports car",
			"sedan",
			"SUV"
		],
		plural:[
			"sports cars",
			"sedans",
			"SUVs"
		]
	},
	super: "cars",
	strength: [1,2,3],
	degree: "height",
	unit: ["feet", "meters"],
	subunit: ["inches", "centimeters"]
},
{
	target: {
		positive: "heavy",
		negative: "light"
	},
	context : [
		" picks up a grape.",
		" picks up an apple.",
		" picks up a watermelon."
	],
	contextWithSuper: [
		" is buying produce in the supermarket and picks up a grape.",
		" is buying produce in the supermarket and picks up an apple.",
		" is buying produce in the supermarket and picks up a watermelon."
	],
	action: [
		"Imagine you pick up a grape.",
		"Imagine you pick up an apple.",
		"Imagine you pick up a watermelon."
	],
	sub: {
		singular: [
			"grape",
			"apple",
			"watermelon"
		],
		plural: [
			"grapes",
			"apples",
			"watermelons"
		]
	},
	super: "fruit",
	strength: [1,2,3],
	degree: "weight",
	unit: ["pounds", "kilograms"],
	subunit: ["ounces", "grams"]
},
{ // This is
	target: {
		positive: " heavy",
		negative: " light"
	},
	context : [
		" lifts up a reading lamp.",
		" lifts up a coffee table.",
		" lifts up a wardrobe."
	],
	contextWithSuper: [
		" is moving furniture and lifts up a reading lamp.",
		" is moving furniture and lifts up a coffee table.",
		" is moving furniture and lifts up a wardrobe.",
	],
	action: [
		"Imagine you pick up a reading lamp.",
		"Imagine you pick up a coffee table.",
		"Imagine you pick up a wardrobe."
	],
	sub: {
		singular: [
			"reading lamp",
			"coffee table",
			"wardrobe"
		],
		plural: [
			"reading lamps",
			"coffee tables",
			"wardrobes"
		]
	},
	super: "furniture",
	strength: [1,2,3],
	degree: "weight",
	unit: ["pounds", "kilograms"],
	subunit: ["ounces", "grams"]
},
{
	target: {
		positive: "loud",
		negative: "quiet"
	},
	context : [
		" takes an electric car for a test-drive.",
		" takes a family car for a test-drive.",
		" takes a muscle car for a test-drive."
	],
	contextWithSuper: [
		" is test-driving cars and takes an electric car for a test-drive.",
		" is test-driving cars and takes a family car for a test-drive.",
		" is test-driving cars and takes a muscle car for a test-drive."
	],
	action: [
		"Imagine taking an electric car for a test-drive.",
		"Imagine taking a family car for a test-drive.",
		"Imagine taking a muscle car for a test-drive."
	],
	sub: {
		singular: [
			"electric car",
			"family car",
			"muscle car"
		],
		plural: [
			"electric cars",
			"family cars",
			"muscle cars"
		]
	},
	super: "cars",
	strength: [1,2,3],
	degree: "sound"
},
{
	target: {
		positive: "light",
		negative: "dark"
	},
	context : [
		" walks into a basement in the middle of the day.",
		" walks into a living room in the middle of the day.",
		" walks into a sunroom in the middle of the day."
	],
	contextWithSuper: [
		" is walking around the rooms of a house and walks into a basement.",
		" is walking around the rooms of a house and walks into a living room.",
		" is walking around the rooms of a house and walks into a sunroom.",
	],
	action: [
		"Imagine walking into a basement.",
		"Imagine walking into a living room.",
		"Imagine walking into a sunroom.",
	],
	sub: {
		singular: [
			"basement",
			"living room",
			"sunroom"
		],
		plural: [
			"basements",
			"living rooms",
			"sunrooms"
		]
	},
	super: "rooms",
	strength: [1,2,3],
	degree: "light"
}];
