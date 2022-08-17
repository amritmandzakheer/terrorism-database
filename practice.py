import streamlit as st
import pandas as pd
import matplotlib
import plotly.express as px

st.set_page_config(layout='wide')

# to run, type "streamlit run practice.py" into the terminal

@st.cache
def get_data():
    terror_df = pd.read_csv(
        r'https://github.com/amritmandzakheer/terrorism-database/blob/92783270c1f83db0aa9b4da1ff1f9bea016dc537/globalterrorism.csv',
        encoding='ISO-8859-1', low_memory=False)
    return terror_df

terror = get_data()

header = st.container()
method = st.container()
descriptive = st.container()
exploratory = st.container()

with header:
    buffer, col1 = st.columns([1, 5])
    with col1:
        st.title("Global Terrorism Analysis")
        st.write("Welcome to Amrit Mandzak-Heer's first data project!")
        st.text(" ")

with method:
    buffer, col1 = st.columns([1, 5])
    with col1:
        st.header("Source and Method")
        st.write(
            "I will be using the Global Terrorism Database (GTD), which is maintained by the National Consortium for "
            "the  \nStudy of Terrorism and Responses to Terrorism (START) at the University of Maryland. The full "
            "database covers a  \ntime period of 1970-2017, includes 181,691 instances and over 100 "
            "attributes.  \nYou can [find the database here.](https://www.start.umd.edu/gtd/)"
            "\n \nMy analysis concerns a subset of that dataset, limited to only 24 attributes "
            "(but otherwise matching the original). "
            "  \nI will perform a descriptive and exploratory analysis. "
            "\n \nFor this analysis, I will employ the python programming language, the pandas and plotly "
            "libraries, and the streamlit web app framework")
        st.text(" ")
        st.subheader("A quick look at the dataset")
        st.caption("Table shows first 20 rows and selected attributes of dataset")
        st.text(" ")

        st.write(terror[['year', 'country', 'region', 'attacktype1', 'targtype', 'nkill', 'nwound']].head(20))
        st.text(" ")

with descriptive:
    buffer, col1 = st.columns([1, 5])
    with col1:
        st.header("Results of Analysis")
        st.write("Here are the results from some common descriptive and exploratory analyses performed on the dataset")
        st.text(" ")
        st.subheader("Summary Statistics")

        sum_kill = terror['nkill'].sum()
        sum_kill_year = terror.groupby('year')['nkill'].sum()
        mean_kill_year = sum_kill_year.mean()
        median_kill_year = sum_kill_year.median()
        std_kill_year = sum_kill_year.std()
        count_events = terror['eventid'].count()
        events_year = terror.groupby('year')['eventid'].count()
        mean_events_year = events_year.mean()
        median_events_year = events_year.median()
        std_events_year = events_year.std()
        sum_wounded = terror['nwound'].sum()
        sum_wound_year = terror.groupby('year')['nkill'].sum()
        mean_wounded_year = sum_wound_year.mean()

        summary = pd.DataFrame(columns=['Statistic', 'Value'],
                               data=[['Total number of events', count_events],
                                     ['Mean number of events per year', mean_events_year],
                                     ['Median number of events per year', median_events_year],
                                     ['Standard deviation of events per year', std_events_year],
                                     ['Total number of casualties', sum_kill],
                                     ['Mean casualties per year', mean_kill_year],
                                     ['Median casualties per year', median_kill_year],
                                     ['Standard deviation casualties per year', std_kill_year],
                                     ['Total number of wounded', sum_wounded],
                                     ['Mean wounded per year', mean_wounded_year]],
                               dtype='int')

        st.write(summary)

        st.text(" ")
        st.write("Given the spread, the measures of central tendency are not particularly informative. "
                 "  \nPlotting the data over time will provide a more valuable analysis.")
        st.text(" ")
        st.subheader("Plotting the Data")

        events_year = pd.DataFrame(terror.groupby('year')['eventid'].count(), dtype='int')

        fig = px.line(data_frame=events_year, x=events_year.index, y=events_year.columns,
                      title='<b>Number of Terrorist Events by Year</b>',
                      labels=dict(eventid='Number of Events', year='Year'),
                      width=900,
                      height=500)
        st.plotly_chart(fig)
        st.write("The large spread can now be explained by the significant increase in terrorist events since "
                 "approximately 2011.")
        st.text(" ")


with exploratory:
    buffer, col1 = st.columns([1, 5])
    with col1:
        st.subheader("Explore Changes over Time")
        st.write("Tracking other attributes over time may also help us answer the following questions:  \n"
             "1) Does the predominant type of attack change over time?  \n"
             "2) Does the location of terrorist attacks change over time?  \n"
             "3) Does the target of terrorist attacks change over time?")
        st.text(" ")

    buffer, col2, col3 = st.columns([1, 4, 1])
    with col3:
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")

        deaths = 'Casualties'
        wounded = 'Wounded'
        attack_type = 'Attack Type'
        location = 'Location of Attack'
        target = 'Target of Attack'
        choice = st.selectbox("Select the Attribute to Track over Time",
                     options=[deaths, wounded, attack_type, location, target])

    with col2:

        def vis_choice(choice):
            if choice == deaths:
                deaths_year = pd.DataFrame(terror.groupby('year')['nkill'].sum(), dtype='int')
                fig2 = px.line(data_frame=deaths_year, x=deaths_year.index, y=deaths_year.columns,
                              title='<b>Number of Casualties by Year</b>',
                              labels=dict(nkill='Number of Casualties', year='Year'),
                              width=900,
                              height=600)
                st.plotly_chart(fig2)
            elif choice == wounded:
                wounded_year = pd.DataFrame(terror.groupby('year')['nwound'].sum(), dtype='int')
                fig3 = px.line(data_frame=wounded_year, x=wounded_year.index, y=wounded_year.columns,
                              title='<b>Number of Wounded by Year</b>',
                              labels=dict(nwound='Number of Wounded', year='Year'),
                              width=930,
                              height=600)
                st.plotly_chart(fig3)
            elif choice == attack_type:
                type_year = pd.DataFrame(terror.groupby(['year', 'attacktype1'])['eventid'].count().unstack())
                fig4 = px.line(data_frame=type_year, x=type_year.index, y=type_year.columns,
                               title='<b>Number of Terrorist Events Grouped by Attack Type by Year</b>',
                               labels=dict(eventid='Number of Events', year='Year'),
                               width=1050,
                               height=600)
                st.plotly_chart(fig4)
            elif choice == location:
                location_year = pd.DataFrame(terror.groupby(['year', 'region'])['eventid'].count().unstack())
                fig5 = px.line(data_frame=location_year, x=location_year.index, y=location_year.columns,
                               title='<b>Number of Terrorist Events Grouped by Region by Year</b>',
                               labels=dict(eventid='Number of Events', year='Year'),
                               width=1050,
                               height=600)
                st.plotly_chart(fig5)
            elif choice == target:
                target_year = pd.DataFrame(terror.groupby(['year', 'targtype'])['eventid'].count().unstack())
                fig6 = px.line(data_frame=target_year, x=target_year.index, y=target_year.columns,
                               title='<b>Number of Terrorist Events Grouped by Target by Year</b>',
                               labels=dict(eventid='Number of Events', year='Year'),
                               width=1050,
                               height=600)
                st.plotly_chart(fig6)
            else:
                st.write("Please make a choice")

        vis_choice(choice)

        st.text(" ")
        st.write("The graphs allow us to answer the above questions and to pose new questions for further research, "
                 "such as:  \n"
                 "1) What explains the rise of Hostage Taking (Kidnapping) over the past ten years, as the third most "
                 "common type of terrorist attack?  \n"
                 "2) Why has the region with the most terrorist attacks for any given period changed so frequently? "
                 "What geopolitical developments does this shift track?  \n"
                 "3) What does the relative stability of the target of terrorist attacks over time reveal "
                 "regarding terrorist strategy and tactics?")
        st.text(" ")
        st.text(" ")

    buffer, col4, col5 = st.columns([1, 4, 1])

    with col5:
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")
        st.text(" ")

        southasia = 'South Asia'
        mideast = 'Middle East & North Africa'
        aussie = 'Australasia & Oceania'
        africa = 'Sub-Saharan Africa'
        s_america = 'South America'
        c_america = 'Central America & Caribbean'
        n_america = 'North America'
        se_asia = 'Southeast Asia'
        w_europe = 'Western Europe'
        e_europe = 'Eastern Europe'
        all = 'All Regions'

        sec_choice = st.radio("Select the Region:",
                              options=[all, aussie, n_america, c_america, s_america, africa, mideast, w_europe, e_europe,
                                       southasia, se_asia])

    with col4:
        st.subheader("Null Results and Asking the Right Questions")
        st.write("Let's consider another question: **Are terrorist attacks more frequent during certain months?**  \n  \n"
                 "The graph below displaying all regions suggests not. But we might have reason to think that viewing all "
                 "regions may obscure  \nsome genuine variation, given different climate, weather, or political patterns "
                 "in different parts of the world. So it may be better  \nto focus on specific regions in asking this "
                 "question.  \n  \nSelect for a particular region to see if there is variation for any particular "
                 "part of the world.")


        def sec_vis_choice(sec_choice):
            if sec_choice == all:
                all_regions = pd.DataFrame(terror.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=all_regions, x=all_regions.index, y=all_regions.columns,
                             title='<b>Number of Terrorist Attacks by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == aussie:
                filter = pd.DataFrame(terror[terror['region']=='Australasia & Oceania'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in Australasia & Oceania by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == n_america:
                filter = pd.DataFrame(terror[terror['region'] == 'North America'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in North America by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == c_america:
                filter = pd.DataFrame(terror[terror['region'] == 'Central America & Caribbean'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in Central America and the Caribbean by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == s_america:
                filter = pd.DataFrame(terror[terror['region'] == 'South America'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in South America by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == africa:
                filter = pd.DataFrame(terror[terror['region'] == 'Sub-Saharan Africa'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in Sub-Saharan Africa by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == mideast:
                filter_mideast = pd.DataFrame(terror[terror['region']=='Middle East & North Africa'])
                mideast_month = pd.DataFrame(filter_mideast.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=mideast_month, x=mideast_month.index, y=mideast_month.columns,
                             title='<b>Number of Terrorist Attacks in the Middle East & North Africa by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == w_europe:
                filter = pd.DataFrame(terror[terror['region'] == 'Western Europe'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in Western Europe by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == e_europe:
                filter = pd.DataFrame(terror[terror['region'] == 'Eastern Europe'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in Eastern Europe by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == southasia:
                filter = pd.DataFrame(terror[terror['region'] == 'South Asia'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in South Asia by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            elif sec_choice == se_asia:
                filter = pd.DataFrame(terror[terror['region'] == 'Southeast Asia'])
                by_month = pd.DataFrame(filter.groupby('month')['eventid'].count())
                fig = px.bar(data_frame=by_month, x=by_month.index, y=by_month.columns,
                             title='<b>Number of Terrorist Attacks in Southeast Asia by Month',
                             width=900,
                             height=600)
                st.plotly_chart(fig)
            else:
                st.write("Please make a choice")


        sec_vis_choice(sec_choice)
        st.text(" ")
        st.write("Organizing the data by region shows that for most regions, there is no significant difference "
                 "in the number of attacks by month. In certain regions, however, such as North America, Eastern "
                 "Europe, and Australasia & Oceania, there does appear to be some difference in the "
                 "number of attacks, depending on time of year.  \n  \n  \n"
                 "Let's consider one more question: **Which types of attack are most lethal?**  \n  \n"
                 "We might initially hypothesize that armed assaults and bombings are most lethal, since "
                 "they often involve large number of civilians and are not targeted to specific individuals. "
                 "However, we must be careful in how we interpret this question, because one way of analyzing the data "
                 "may yield this: ")

        attacktype_death = pd.DataFrame(terror.groupby('attacktype1')['nkill'].sum())
        fig_a = px.bar(data_frame=attacktype_death, x=attacktype_death.index, y=attacktype_death.columns,
                     title="<b> Number of Casualties by Attack Type",
                     width=900,
                     height=600)
        st.plotly_chart(fig_a)

        st.text(" ")
        st.write("This chart seems to confirm our hypothesis - armed assaults and bombings are the most lethal. "
                 "But this chart is misleading, at least if what we are really interested in is whether a particular "
                 "attack type in itself tends to be more lethal. This chart tells us the total number of "
                 "casualties for each attack type. But since we've already seen that some attack types are more "
                 "common than others, the difference in the total may be partially a result of the number of events "
                 "for each. We will therefore want to consider the mean number of casualties for each attack "
                 "type  \n  \nHere is a chart displaying that:")

        attacktype_mean_death = pd.DataFrame(terror.groupby('attacktype1')['nkill'].mean())
        fig_b = px.bar(data_frame=attacktype_mean_death, x=attacktype_mean_death.index,
                       y=attacktype_mean_death.columns,
                       title='<b>Mean Number of Casualties by Attack Type',
                       width=900,
                       height=600)
        st.plotly_chart(fig_b)

        st.text(" ")
        st.write("From this chart, we can see that our hypothesis was way off, Hijacking is the most lethal type of "
                 "terrorist attack, with Hostage Taking (Barricade) the second most. And while armed assaults are the "
                 "third most lethal type of attack (excluding unknowns), bombings are relatively less lethal "
                 "compared to others.")
        st.text(" ")
        st.subheader("Final Note")
        st.write("I hope you enjoyed my first attempt at organizing, analyzing, and visualising data!  \n  \n"
                 "I've got a lot still to learn on each of these areas, so go check back at my site to see "
                 "any new projects that I may post.")


