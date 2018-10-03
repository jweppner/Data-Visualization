#!/usr/bin/env python
# coding: utf-8

# ## World Progress

# In[1]:


from datascience import *
import numpy as np

get_ipython().run_line_magic('matplotlib', 'inline')
import matplotlib.pyplot as plots
plots.style.use('fivethirtyeight')

from client.api.notebook import Notebook
ok = Notebook('project1.ok')
_ = ok.auth(inline=True)


# ## 1. Global Population Growth
# 

# The global population of humans reached 1 billion around 1800, 3 billion around 1960, and 7 billion around 2011. The potential impact of exponential population growth has concerned scientists, economists, and politicians alike.
# 
# The UN Population Division estimates that the world population will likely continue to grow throughout the 21st century, but at a slower rate, perhaps reaching 11 billion by 2100. However, the UN does not rule out scenarios of more extreme growth.
# 
# <a href="http://www.pewresearch.org/fact-tank/2015/06/08/scientists-more-worried-than-public-about-worlds-growing-population/ft_15-06-04_popcount/"> 
#  <img src="pew_population_projection.png"/> 
# </a>
# 
# In this section, we will examine some of the factors that influence population growth and how they are changing around the world.
# 
# The first table we will consider is the total population of each country over time. Run the cell below.

# In[3]:


population = Table.read_table('population.csv')
population.show(3)


# ### Bangladesh
# 
# In the `population` table, the `geo` column contains three-letter codes established by the [International Organization for Standardization](https://en.wikipedia.org/wiki/International_Organization_for_Standardization) (ISO) in the [Alpha-3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#Current_codes) standard. We will begin by taking a close look at Bangladesh. Inspect the standard to find the 3-letter code for Bangladesh.

# **Question 1.** Create a table called `b_pop` that has two columns labeled `time` and `population_total`. The first column should contain the years from 1970 through 2015 (including both 1970 and 2015) and the second should contain the population of Bangladesh in each of those years.

# In[3]:


b_pop_1 = population.select('time', 'population_total', 'geo')
b_pop = b_pop_1.where('geo', are.equal_to('bgd')).drop('geo').where('time', are.above_or_equal_to(1970)).where('time', are.below_or_equal_to(2015))
b_pop


# In[4]:


_ = ok.grade('q1_1')


# Run the following cell to create a table called `b_five` that has the population of Bangladesh every five years. At a glance, it appears that the population of Bangladesh has been growing quickly indeed!

# In[5]:


b_pop.set_format('population_total', NumberFormatter)

fives = np.arange(1970, 2016, 5) # 1970, 1975, 1980, ...
b_five = b_pop.sort('time').where('time', are.contained_in(fives))
b_five


# **Question 2.** Assign `b_1970_through_2010` to a table that has the same columns as `b_five` and has one row for every five years from 1970 through 2010 (but not 2015). Then, use that table to assign `initial` to an array that contains the population for every five year interval from 1970 to 2010. Finally, assign `changed` to an array that contains the population for every five year interval from 1975 to 2015.
# 
# *Hint*: You may find the `exclude` method to be helpful ([Docs](http://data8.org/datascience/_autosummary/datascience.tables.Table.exclude.html)).

# In[6]:


b_1970_through_2010 = b_five.exclude(9)
initial = b_1970_through_2010.column('population_total')
changed = b_five.exclude(0).column('population_total')


# We have provided the code below that uses `b_1970_through_2010`, `initial`, and `changed` in order to add a column to the table called `annual_growth`. Don't worry about the calculation of the growth rates; run the test below to test your solution.
# 
# If you are interested in how we came up with the formula for growth rates, consult the [growth rates](https://www.inferentialthinking.com/chapters/03/2/1/growth) section of the textbook.

# In[7]:


b_five_growth = b_1970_through_2010.with_column('annual_growth', (changed/initial)**0.2-1)
b_five_growth.set_format('annual_growth', PercentFormatter)


# In[8]:


_ = ok.grade('q1_2')


# While the population has grown every five years since 1970, the annual growth rate decreased dramatically from 1985 to 2005. Let's look at some other information in order to develop a possible explanation. Run the next cell to load three additional tables of measurements about countries over time.

# In[9]:


life_expectancy = Table.read_table('life_expectancy.csv')
child_mortality = Table.read_table('child_mortality.csv').relabeled(2, 'child_mortality_under_5_per_1000_born')
fertility = Table.read_table('fertility.csv')


# The `life_expectancy` table contains a statistic that is often used to measure how long people live, called *life expectancy at birth*. This number, for a country in a given year, [does not measure how long babies born in that year are expected to live](http://blogs.worldbank.org/opendata/what-does-life-expectancy-birth-really-mean). Instead, it measures how long someone would live, on average, if the *mortality conditions* in that year persisted throughout their lifetime. These "mortality conditions" describe what fraction of people at each age survived the year. So, it is a way of measuring the proportion of people that are staying alive, aggregated over different age groups in the population.

# Run the following cells below to see `life_expectancy`, `child_mortality`, and `fertility`. Refer back to these tables as they will be helpful for answering further questions!

# In[10]:


life_expectancy


# In[11]:


child_mortality


# In[12]:


fertility


# **Question 3.** Perhaps population is growing more slowly because people aren't living as long. Use the `life_expectancy` table to draw a line graph with the years 1970 and later on the horizontal axis that shows how the *life expectancy at birth* has changed in Bangladesh.

# In[13]:


life1 = life_expectancy.where('time', are.above(1970))
life2 = life1.where('geo', are.equal_to('bgd'))
life2.plot('time', 'life_expectancy_years')


# **Question 4.** Assuming everything else stays the same, does the graph above help directly explain why the population growth rate decreased from 1985 to 2010 in Bangladesh? Why or why not? What happened in Bangladesh in 1991, and does that event explain the change in population growth rate?

# No, it does not. If anything, a higher life expectancy would contribute to a higher growth rate amongst the population as the population size would increase due to people living longer lives. 
# It seems that in 1991 there was a sudden drop in life expectancy. This could be a result of, for example, a natural disaster in which a large portion of newborns weren't able to receive adequate medical care. It does not help explain the decreasing growth rate, as the cause seemingly had no long-term effect on the increasing life expectancy.

# The `fertility` table contains a statistic that is often used to measure how many babies are being born, the *total fertility rate*. This number describes the [number of children a woman would have in her lifetime](https://www.measureevaluation.org/prh/rh_indicators/specific/fertility/total-fertility-rate), on average, if the current rates of birth by age of the mother persisted throughout her child bearing years, assuming she survived through age 49. 

# **Question 5.** Write a function `fertility_over_time` that takes the Alpha-3 code of a `country` and a `start` year. It returns a two-column table with labels "`Year`" and "`Children per woman`" that can be used to generate a line chart of the country's fertility rate each year, starting at the `start` year. The plot should include the `start` year and all later years that appear in the `fertility` table. 
# 
# Then, in the next cell, call your `fertility_over_time` function on the Alpha-3 code for Bangladesh and the year 1970 in order to plot how Bangladesh's fertility rate has changed since 1970. Note that the function `fertility_over_time` should not return the plot itself **The expression that draws the line plot is provided for you; please don't change it.**

# In[14]:


def fertility_over_time(country, start):
    """Create a two-column table that describes a country's total fertility rate each year."""
    country_fertility = fertility.where('geo', are.equal_to(country))
    country_fertility_after_start = country_fertility.where('time', are.above_or_equal_to(start))
    return country_fertility_after_start.select(1, 2).relabel('time', 'Year').relabel('children_per_woman_total_fertility', 'Children per woman')


# In[15]:


bangladesh_code = 'bgd'
fertility_over_time(bangladesh_code, 1970).plot(0, 1) # You should *not* change this line.


# In[16]:


_ = ok.grade('q1_5')


# **Question 6.** Assuming everything else stays the same, does the graph above help directly explain why the population growth rate decreased from 1985 to 2010 in Bangladesh? Why or why not?

# It does, since it clearly indicates that a woman has become increasingly more likely to have less kids from 1970 - 2010. Therefore, less children are born, decreasing the growth rate.

# It has been observed that lower fertility rates are often associated with lower child mortality rates. The link has been attributed to family planning: if parents can expect that their children will all survive into adulthood, then they will choose to have fewer children. We can see if this association is evident in Bangladesh by plotting the relationship between total fertility rate and [child mortality rate per 1000 children](https://en.wikipedia.org/wiki/Child_mortality).

# **Question 7.** Using both the `fertility` and `child_mortality` tables, draw a scatter diagram with one point for each year, starting with 1970, that has Bangladesh's total fertility on the horizontal axis and its child mortality on the vertical axis. 
# 
# **The expression that draws the scatter diagram is provided for you; please don't change it.** Instead, create a table called `post_1969_fertility_and_child_mortality` with the appropriate column labels and data in order to generate the chart correctly. Use the label "`Children per woman`" to describe total fertility and the label "`Child deaths per 1000 born`" to describe child mortality.

# In[17]:


bgd_fertility = fertility.where('geo', are.equal_to('bgd'))
bgd_child_mortality = child_mortality.where('geo', are.equal_to('bgd'))

fertility_and_child_mortality = bgd_fertility.join('time', bgd_child_mortality, 'time')

post_1969_fertility_and_child_mortality = fertility_and_child_mortality.where('time', are.above_or_equal_to(1970)).drop('geo_2').relabel('children_per_woman_total_fertility', 'Children per woman').relabel('child_mortality_under_5_per_1000_born', 'Child deaths per 1000 born')
post_1969_fertility_and_child_mortality.scatter('Children per woman', 'Child deaths per 1000 born') # You should *not* change this line.


# In[18]:


_ = ok.grade('q1_7')


# **Question 8.** In one or two sentences, describe the association (if any) that is illustrated by this scatter diagram. Does the diagram show that reduced child mortality causes parents to choose to have fewer children?

# The scatterplot shows a liner association between the two variables. The plot could induce that when there are less child deaths a woman will choose to have less children, since if a child passes away, the woman might be more likely to choose to have another child. However, the plot could also indicate that when woman have more children, more children deaths per 1000 born occur. This could be a result of, for example, having more children would lead to less attentiont per individual child or even less life essential resources for each child due to a larger family size. Either hypothesis seems feasible, but one cannot be certain based off solely the scatterplot. 

# ### The World
# 
# The change observed in Bangladesh since 1970 can also be observed in many other developing countries: health services improve, life expectancy increases, and child mortality decreases. At the same time, the fertility rate often plummets, and so the population growth rate decreases despite increasing longevity.

# Run the cell below to generate two overlaid histograms, one for 1960 and one for 2010, that show the distributions of total fertility rates for these two years among all 201 countries in the `fertility` table.

# In[19]:


Table().with_columns(
    '1960', fertility.where('time', 1960).column(2),
    '2010', fertility.where('time', 2010).column(2)
).hist(bins=np.arange(0, 10, 0.5), unit='child')
_ = plots.xlabel('Children per woman')
_ = plots.xticks(np.arange(10))


# **Question 9.** Assign `fertility_statements` to a list of the numbers of each statement below that can be correctly inferred from these histograms.
# 1. About the same number of countries had a fertility rate between 3.5 and 4.5 in both 1960 and 2010.
# 1. In 2010, about 40% of countries had a fertility rate between 1.5 and 2 (inclusive).
# 1. In 1960, less than 20% of countries had a fertility rate below 3.
# 1. More countries had a fertility rate above 3 in 1960 than in 2010.
# 1. At least half of countries had a fertility rate between 5 and 8 (inclusive) in 1960.
# 1. At least half of countries had a fertility rate below 3 in 2010.

# In[20]:


fertility_statements = [1, 3, 4, 5, 6]


# In[21]:


_ = ok.grade('q1_9')


# **Question 10.** Draw a line plot of the world population from 1800 through 2005. The world population is the sum of all the country's populations. 

# In[22]:


total_pop = population.group('time', sum).drop('geo sum').sort('time', descending=True).where('time', are.below(2006)).where('time', are.above(1799))
total_pop.plot('time')


# **Question 11.** Create a function `stats_for_year` that takes a `year` and returns a table of statistics. The table it returns should have four columns: `geo`, `population_total`, `children_per_woman_total_fertility`, and `child_mortality_under_5_per_1000_born`. Each row should contain one Alpha-3 country code and three statistics: population, fertility rate, and child mortality for that `year` from the `population`, `fertility` and `child_mortality` tables. Only include rows for which all three statistics are available for the country and year.
# 
# In addition, restrict the result to country codes that appears in `big_50`, an array of the 50 most populous countries in 2010. This restriction will speed up computations later in the project.
# 
# *Hint*: The tests for this question are quite comprehensive, so if you pass the tests, your function is probably correct. However, without calling your function yourself and looking at the output, it will be very difficult to understand any problems you have, so try your best to write the function correctly and check that it works before you rely on the `ok` tests to confirm your work.

# In[23]:


# We first create a population table that only includes the 
# 50 countries with the largest 2010 populations. We focus on 
# these 50 countries only so that plotting later will run faster.

big_50 = population.where('time', 2010).sort(2, descending=True).take(np.arange(50)).column('geo')
population_of_big_50 = population.where('time', are.above(1959)).where('geo', are.contained_in(big_50))

def stats_for_year(year):
    """Return a table of the stats for each country that year."""
    p = population_of_big_50.where('time', year).drop('time')
    f = fertility.where('time', year).drop('time')
    c = child_mortality.where('time', year).drop('time')
    return p.join('geo', f, 'geo').join('geo', c, 'geo')


# Try calling your function `stats_for_year` on any year between 1960 and 2010 in the cell below.  Try to understand the output of `stats_for_year`.

# In[24]:


stats_for_year(2002)


# In[25]:


_ = ok.grade('q1_11')


# **Question 12.** Create a table called `pop_by_decade` with two columns called `decade` and `population`. It has a row for each `year` since 1960 that starts a decade. The `population` column contains the total population of all countries included in the result of `stats_for_year(year)` for the first `year` of the decade. For example, 1960 is the first year of the 1960's decade. You should see that these countries contain most of the world's population.
# 
# *Hint:* One approach is to define a function `pop_for_year` that computes this total population, then `apply` it to the `decade` column.  The `stats_for_year` function from the previous question may be useful here.
# 
# **Note:** The `pop_by_decade` cell is directly below the cell containing the helper function `pop_for_year`. This is where you will generate the `pop_by_decade` table!

# In[26]:


#create table 'pop_by_decade' with two columns --> (1) decade & (2) population
    #has a row for each year since 1960 that starts a decade
    #population column contains the total population of all countries in fn stats_for_year(year)     

def pop_for_year(year):
    return sum(stats_for_year(year).column('population_total'))



# This test is just a sanity check for your helper function if you choose to use it. You will not lose points for not implementing the function `pop_for_year`.

# In[27]:


_ = ok.grade('q1_12_0')


# In[28]:


decades = Table().with_column('decade', np.arange(1960, 2011, 10))
decades_array = decades.apply(pop_for_year, 'decade')

pop_by_decade = decades.with_column('population', decades_array)
pop_by_decade.set_format(1, NumberFormatter)


# In[29]:


_ = ok.grade('q1_12')


# The `countries` table describes various characteristics of countries. The `country` column contains the same codes as the `geo` column in each of the other data tables (`population`, `fertility`, and `child_mortality`). The `world_6region` column classifies each country into a region of the world. Run the cell below to inspect the data.

# In[30]:


countries = Table.read_table('countries.csv').where('country', are.contained_in(population.group('geo').column(0)))
countries.select('country', 'name', 'world_6region')


# **Question 13.** Create a table called `region_counts` that has two columns, `region` and `count`. It should describe the count of how many countries in each region appear in the result of `stats_for_year(1960)`. For example, one row would have `south_asia` as its `world_6region` value and an integer as its `count` value: the number of large South Asian countries for which we have population, fertility, and child mortality numbers from 1960.

# In[31]:


r_c = stats_for_year(1960).join('geo', countries, 'country')
region_counts = r_c.group('world_6region').relabel('world_6region', 'region')
region_counts


# In[32]:


_ = ok.grade('q1_13')


# The following scatter diagram compares total fertility rate and child mortality rate for each country in 1960. The area of each dot represents the population of the country, and the color represents its region of the world. Run the cell. Do you think you can identify any of the dots?

# In[33]:


from functools import lru_cache as cache

# This cache annotation makes sure that if the same year
# is passed as an argument twice, the work of computing
# the result is only carried out once.
@cache(None)
def stats_relabeled(year):
    """Relabeled and cached version of stats_for_year."""
    return stats_for_year(year).relabeled(2, 'Children per woman').relabeled(3, 'Child deaths per 1000 born')

def fertility_vs_child_mortality(year):
    """Draw a color scatter diagram comparing child mortality and fertility."""
    with_region = stats_relabeled(year).join('geo', countries.select('country', 'world_6region'), 'country')
    with_region.scatter(2, 3, sizes=1, colors=4, s=500)
    plots.xlim(0,10)
    plots.ylim(-50, 500)
    plots.title(year)

fertility_vs_child_mortality(1960)


# **Question 14.** Assign `scatter_statements` to a list of the numbers of each statement below that can be inferred from this scatter diagram for 1960. 
# 1. The `europe_central_asia` region had the lowest child mortality rate.
# 1. The lowest child mortality rate of any country was from an `east_asian_pacific` country.
# 1. Most countries had a fertility rate above 5.
# 1. There was an association between child mortality and fertility.
# 1. The two largest countries by population also had the two highest child mortality rate.

# In[34]:


scatter_statements = [1, 3, 4]


import ipywidgets as widgets

Table().with_column('Year', np.arange(1960, 2016)).apply(stats_relabeled, 'Year')

_ = widgets.interact(fertility_vs_child_mortality, 
                     year=widgets.IntSlider(min=1960, max=2015, value=1960))


population = Table.read_table('population.csv')
countries = Table.read_table('countries.csv').where('country', are.contained_in(population.group('geo').column(0)))
poverty = Table.read_table('poverty.csv')
poverty.show(3)


def first(values):
    return values.item(0)

pp = poverty.sort('time', descending=True)
latest_poverty = pp.group('geo', first)

latest_poverty.relabel(0, 'geo').relabel(1, 'time').relabel(2, 'poverty_percent') # You should *not* change this line.


pop = population.where('time', 2010)

p_a_p = latest_poverty.join('geo', pop)
p_t = (p_a_p.column(('poverty_percent')) * p_a_p.column('population_total')) /100

recent_poverty_total = p_a_p.with_column('poverty_total', np.round(p_t)).drop('time_2').drop('time')
recent_poverty_total


world_poverty = sum(recent_poverty_total.column('poverty_total'))

world_population_2010 = population.where('time', are.equal_to(2010))
world_population = sum(world_population_2010.column('population_total'))

poverty_percent = ((world_poverty / world_population) * 100)
poverty_percent


countries.select('country', 'name', 'world_4region', 'latitude', 'longitude')

# In[45]:


countries_2 = countries.select('latitude', 'longitude', 'country', 'name', 'world_4region', )
poverty_map = countries_2.join('country', recent_poverty_total, 'geo').drop('country').drop('population_total').drop('poverty_percent').relabel('world_4region', 'region')
poverty_map

colors = {'africa': 'blue', 'europe': 'black', 'asia': 'red', 'americas': 'green'}
scaled = poverty_map.with_column(
    'poverty_total', 2e4 * poverty_map.column('poverty_total'),
    'region', poverty_map.apply(colors.get, 'region')
)
Circle.map_table(scaled)


largest = poverty_map.sort('poverty_total', descending=True).take(np.arange(0,10)).select('name', 'poverty_total')
largest


def population_for_country_in_year(row_of_poverty_table):
    year = row_of_poverty_table.item('time')
    country = row_of_poverty_table.item('geo')
    return population.where('time', year).where('geo', country).column(2).item(0) 

def poverty_timeline(country):
    country_name_tag = countries.where('name', country).column(0).item(0) 
    pov = poverty.where('geo', country_name_tag) 
    pov_1 = Table().with_column('Year', pov.column(1))
    pov_2 = pov_1.with_columns('Number in poverty', pov.column(2) / 100 * pov.apply(population_for_country_in_year)) 
    pov_2.plot('Year', 'Number in poverty') 


# # Finally, draw the timelines below to see how the world is changing. You can check your work by comparing your graphs to the ones on [gapminder.org](https://goo.gl/lPujuh).

# In[89]:


poverty_timeline('India')


# In[90]:


poverty_timeline('Nigeria')


# In[91]:


poverty_timeline('China')


# In[92]:


poverty_timeline('United States')

all_countries = poverty_map.column('name')
_ = widgets.interact(poverty_timeline, country=list(all_countries))




