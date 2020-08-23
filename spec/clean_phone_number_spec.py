from expects import equal, expect
from mamba import description, it

from src.utils import clean_phone_number

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
