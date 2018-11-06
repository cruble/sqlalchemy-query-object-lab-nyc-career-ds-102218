from sqlalchemy import create_engine, func, or_, desc
from seed import Company
from sqlalchemy.orm import sessionmaker
import pdb; 

engine = create_engine('sqlite:///dow_jones.db', echo=True)
Session = sessionmaker(bind=engine)
session = Session()

def return_apple():
	return session.query(Company).filter(Company.company == "Apple").first()

def return_disneys_industry():
	disney = session.query(Company).filter(Company.company == "Walt Disney").first()	
	return disney.industry

def return_list_of_company_objects_ordered_alphabetically_by_symbol():
	return session.query(Company).order_by(Company.symbol).all()

def return_list_of_dicts_of_tech_company_names_and_their_EVs_ordered_by_EV_descending():
	# d_list = []
	# tech_list = list(session.query(Company).filter(Company.industry == 'Technology').order_by(desc(Company.enterprise_value)))
	# for company in tech_list: 
	# 	tech_dict = {}
	# 	tech_dict[company.company] = company.enterprise_value
	# 	d_list.append(tech_dict)
	# return d_list
	# my failed version ^^^^^ but I just misunderstood the question for correct output format 
	tech = session.query(Company).filter_by(industry='Technology').order_by(Company.enterprise_value.desc())
	arr = []
	for co in tech:
		obj = {'company': co.company, 'EV': co.enterprise_value}
		arr.append(obj)
	return arr

def return_list_of_consumer_products_companies_with_EV_above_225():
	# return list(session.query(Company).filter(Company.enterprise_value > 225, Company.industry == "Consumer products"))
	# this is my first and unsuccessful attempt. the answer wanted a list of dicts
	arr = []
	for company in session.query(Company).filter(Company.industry=='Consumer products', Company.enterprise_value>225).all():
		arr.append({'name': company.company})
	return arr


def return_conglomerates_and_pharmaceutical_companies():
	c_l =  list(session.query(Company).filter(or_(Company.industry == 'Pharmaceuticals', Company.industry == "Conglomerate")))
	return [item.company for item in c_l]

def avg_EV_of_dow_companies():
	return list(session.query(func.avg(Company.enterprise_value)))[0]
	# ev_list = list(session.query(Company.enterprise_value))
	# flattened_evs = [item[0] for item in ev_list]
	# return sum(flattened_evs) / len(flattened_evs)
	# list(session.query(func.sum(Company.enterprise_value).filter(Company.industry == "Pharmaceuticals")))

def ev_of_bc():
	return session.query(func.sum(Company.enterprise_value)).filter(Company.industry == 'Broadcasting and entertainment').scalar()


def return_industry_and_its_total_EV():
	return session.query(Company.industry, func.sum(Company.enterprise_value)).group_by(Company.industry).all()
	# indust_dict = {}
	# industry_list = list(session.query(Company.industry).distinct())
	# cleaned_industry_list = [item[0].replace(u'\xa0', u' ') for item in industry_list]
	# for industry in cleaned_industry_list: 
	# 	indust_dict[industry] = session.query(func.sum(Company.enterprise_value)).filter(Company.industry == industry).scalar()
	# return indust_dict
