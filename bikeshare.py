import time
import pandas as pd
import numpy as np

"""
   Set this variable to False to run normal, Set to True to run unit tests
"""
UNIT_TEST = False

CITY_DATA = {'chicago':       'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington':    'washington.csv'}


def get_data(iter_list, include_all, text):
    """
    Helps return item from a supplied list.
    Args:
        (list) iter_list   - list to search for specified text in.
        (bool) include_all - True if 'all' is a valid option
                              False if 'all' is not a valid option
        (str)  text        - Test to search for in specified list.
                              This text is also used in the prompt.
    Returns:
        (str) data - item desired from supplied list
    """
    data = 'none'
    while ((not (data in iter_list)) and ((not include_all) or (data != 'all'))):
        if include_all:
            data = input('Please select the {} for the data'.format(text) + '(valid choices are: ' + ', '.join(
                iter_list) + ', all): ')
            print()
        else:
            data = input('Please select the {} for the data'.format(text) + '(valid choices are: ' + ', '.join(
                iter_list) + '): ')
            print()
        data = data.lower()
        if ((not (data in iter_list)) and ((not include_all) or (data != 'all'))):
            print("{} is not a valid option!".format(data))

    return data


def column_exists(column, df):
    """
    Simple check if a column is not in a dataframe
    Args:
        (str)       column - text for column to find.
        (dataFrame) df     - Pandas dataFrame to search for column in
    Returns:
        (bool)      comp   - True if column exists, False if not
    Side Effect:
         prints a message if column does not exist.
    """
    comp = column in df.columns
    if not comp:
        print()
        print('No {} information available!'.format(column))
        print()
    return (comp)


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    cities = [*CITY_DATA]
    city = get_data(cities, False, 'city')

    # get user input for month (all, january, february, ... , june)
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month = get_data(months, True, 'month')

    # get user input for day of week (all, monday, tuesday, ... sunday)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day = get_data(days, True, 'day')

    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city  - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day   - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # read in specified datafile.
    df = pd.read_csv(CITY_DATA[city])
    #  the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print()
    print('Most common month: {}'.format(df['month'].mode()[0]))
    print()

    # display the most common day of week
    print()
    print('Most common day of week: {}'.format(df['day_of_week'].mode()[0]))
    print()

    # display the most common start hour
    print()
    print('Most common hour: {}'.format(df['Start Time'].mode()[0]))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print()
    print('Most common used start station: {}'.format(df['Start Station'].mode()[0]))
    print()

    # display most commonly used end station
    print()
    print('Most common used end station: {}'.format(df['End Station'].mode()[0]))
    print()

    # display most frequent combination of start station and end station trip
    print()
    print('most frequent combination of start station and end station trip: {}'.format(
        (df['Start Station'] + ' : ' + df['End Station']).mode()[0]))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print()
    print('Total Travel time: {}'.format(df['Trip Duration'].sum()))
    print()

    # display mean travel time
    print()
    print('Mean Travel time: {}'.format(df['Trip Duration'].mean()))
    print()

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    if column_exists('User Type', df):
        print('Here are the number of users by type:')
        print(df['User Type'].value_counts().to_string())
        print()

    # Display counts of gender
    if column_exists('Gender', df):
        print('Here are the number of users by gender:')
        print(df['Gender'].value_counts().to_string())
        print()

    # Display earliest, most recent, and most common year of birth
    if column_exists('Birth Year', df):
        print('The earliest birth year is {}.'.format(df['Birth Year'].min()))
        print('The most recent birth year is {}.'.format(df['Birth Year'].max()))
        print('The most common birth year is {}'.format(df['Birth Year'].mode()[0]))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' * 40)


def yes_no_prompt(text):
    """
    Helper function to display a yes or no prompt

    Args:
        (str)  text  - Text to display in prompt.
    Returns:
        (bool) True  - yes has been selected
               False - no has been selected
    """
    choice = 'bad'
    while ((choice != 'yes') and (choice != 'no')):
        choice = input('\n{} Enter yes or no.\n'.format(text))
        choice = choice.lower()
    return (choice == 'yes')


def show_raw_data(df):
    """
    Display dataFrame 4 rows or less at a time if user requests

    Args:
        (dataFrame)  df  - Pandas dataFram to display
    """
    index = 0
    block_size = 4
    while (yes_no_prompt('Would you like to see the raw data?') and (index < df.size)):
        for idx in range(index, index + block_size):
            print(df.iloc[idx])
        if ((index + block_size) >= df.size):
            block_size = df.size - index - 1;
        index += block_size


def main():
    if UNIT_TEST:
        """
            This code runs through all simple permutations for the load_data() function.
            It then calls the other functions based on the returned dataframe.
        """
        cities = ['chicago', 'new york city', 'washington']
        months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
        days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for city in cities:
            for month in months:
                for day in days:
                    print('\nTest {},{},{}\n'.format(city, month, day))
                    df = load_data(city, month, day)
                    time_stats(df)
                    station_stats(df)
                    trip_duration_stats(df)
                    user_stats(df)
    else:
        while True:
            city, month, day = get_filters()
            df = load_data(city, month, day)

            """ Ask user if they would like to see raw data """
            show_raw_data(df)

            time_stats(df)
            station_stats(df)
            trip_duration_stats(df)
            user_stats(df)

            if not yes_no_prompt('Would you like to restart?'):
                break

if __name__ == "__main__":
    main()
