from expects import equal, expect
from mamba import description, it

from src.utils import clean_mx_with_regex, clean_phone_number

with description(clean_phone_number) as self:

    with it('clean with whitespaces start and end'):
        result = clean_phone_number('   5510300000   ')
        expect(result).to(equal('5510300000'))

    with it('clean with whitespaces start, end and inside'):
        result = clean_phone_number(' +52 55 10 30 00 00  ')
        expect(result).to(equal('+525510300000'))

    with it('clean with whitespaces inside'):
        result = clean_phone_number('+52 55 10 30 00 00')
        expect(result).to(equal('+525510300000'))


with description(clean_mx_with_regex) as self:

    with it('clean with +521'):
        result = clean_mx_with_regex('+5214491121594')
        expect(result).to(equal('4491121594'))

    with it('clean with +52'):
        result = clean_mx_with_regex('+524491121594')
        expect(result).to(equal('4491121594'))

    with it('clean with whitespaces inside'):
        result = clean_mx_with_regex('4491121594')
        expect(result).to(equal('4491121594'))
