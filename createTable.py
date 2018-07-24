import dbPostgres


def create_current_table():
    dbPostgres.create('public.current_temperature', 'site integer', 'timestamp_measured timestamp without time zone',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.current_condition', 'site integer', 'timestamp_measured timestamp without time zone',
                      'value character varying', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.current_temperature_feels', 'site integer', 'timestamp_measured timestamp without time zone',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.current_pressure', 'site integer', 'timestamp_measured timestamp without time zone',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.current_humidity', 'site integer', 'timestamp_measured timestamp without time zone',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')

def create_calendar_table():
    # создание таблиц данных для утренний показаний
    dbPostgres.create('public.calendar_T_morning_minimum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_morning_maximum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_morning_condition', 'site integer', 'date_calendar date',
                      'value character varying', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_morning_pressure', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_morning_humidity', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_morning_feeling', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    
    # создание таблиц данных для дневных показаний
    dbPostgres.create('public.calendar_T_day_minimum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_day_maximum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_day_condition', 'site integer', 'date_calendar date',
                      'value character varying', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_day_pressure', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_day_humidity', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_day_feeling', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    
    # создание таблиц данных для вечерних показаний
    dbPostgres.create('public.calendar_T_evening_minimum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_evening_maximum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_evening_condition', 'site integer', 'date_calendar date',
                      'value character varying', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_evening_pressure', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_evening_humidity', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_evening_feeling', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    
    # создание таблиц данных для ночных показаний
    dbPostgres.create('public.calendar_T_night_minimum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_night_maximum', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_night_condition', 'site integer', 'date_calendar date',
                      'value character varying', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_night_pressure', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_night_humidity', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')
    dbPostgres.create('public.calendar_T_night_feeling', 'site integer', 'date_calendar date',
                      'value integer', 'timestamp_record timestamp without time zone DEFAULT now()')


def create_system_table():
    dbPostgres.create('public.sysinfo', "site integer", 'timestamp_record timestamp without time zone DEFAULT now()')