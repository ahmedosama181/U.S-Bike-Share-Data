import time
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['sunday', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'all']
def get_filters():

    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Please enter Chicago, Washington or New York City for your analysis')
        city = city.lower()
        if city in CITY_DATA.keys():
            break
        else:
            print('Please enter a valid city name! ')
            continue

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('"Enter any one of the first 6 months or enter All to select all 6 months."')
        month = month.lower().strip()
        if month in months:
            break
        else:
            print('Please enter a valid month! ')
            continue

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Enter the day, or "all" to apply no day filter')
        day = day.lower().strip()
        if day in days:
            break
        else:
            print('Please enter a valid day! ')
            continue
            
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])
    month_filtered = False
    day_filtered = False
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        month_filtered = True
        # use the index of the months list to get the corresponding int
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        day_filtered = True
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df, month_filtered, day_filtered


def time_stats(df, month_filtered, day_filtered):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # display the most common month
    # if the data was not filtered by month
    if month_filtered == False:
        common_month = df['month'].mode()[0]
        common_month = months[common_month -1]
        print('Most Common Month: {}'.format(common_month))
    # display the most common day of week
    # if the data was not filtered by day
    if day_filtered == False:
        common_day = df['day_of_week'].mode()[0]
        print('Most Common Day:', common_day)

    # display the most common start hour
    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most common hour (from 0 to 23)
    popular_hour = df['hour'].mode()[0]

    print('Most Frequent Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print('The Most Common Start Stations:  ', common_start_station, '\n')

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print('The Most Common End Stations:  ', common_end_station)
    # display most frequent combination of start station and end station trip

    common_combination = (df['Start Station'] +' , '+df['End Station']).mode()[0]
    print('\n The Most Common Combination:  ', common_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('\nTotal Travel Time: ', total_travel_time)
    # display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('\nAverage Travel Time: ', mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts = df['User Type'].value_counts()
    print('\nCounts Of User Types:\n', user_type_counts.to_string())

    # Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print('\nCounts Of Genders:\n', gender_counts.to_string())
    except:
        print('\nThere is no Gender column in this dataset')
    # Display earliest, most recent, and most common year of birth
    try:
        earliest_year = int(df['Birth Year'].min())
        most_recent_year = int(df['Birth Year'].max())
        most_common_year = int(df['Birth Year'].mode()[0])
        print('\nThe Earliest Birth Year: ', earliest_year
              , '\nThe Most Recent Birth Year: ', most_recent_year
              , '\nThe Most Common Birth Year: ', most_common_year)

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
    except:
        print('\nThere is no Birth Year column in this dataset')

# here we can display 5 rows of individual trips 
# data depending on the user raw input
def display_data(df):
    # get user input
    view_data = input("Would you like to view 5 rows of individual trip data? Enter yes or no?").lower()
    start_loc = 0
    # while the user is entering yes 
    # continue displaying 5 more rows
    while (view_data == 'yes'):
        # print data starting from the last start_loc 
        print(df.iloc[start_loc:start_loc+5].to_string())
        start_loc += 5
        # asking the user if he wants to continue
        view_display = input("Do you wish to continue?: ").lower()
        if view_display != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        df, month_filtered, day_filtered = load_data(city, month, day)
        time_stats(df, month_filtered, day_filtered)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break



if __name__ == "__main__":
	main()
