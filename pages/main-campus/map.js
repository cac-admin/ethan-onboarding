import  {Container}  from '@mui/material';
import {Typography} from '@mui/material';
import {Button} from '@mui/material';
import Link from 'next/link';
import Head from 'next/head';

export default function MainMap() {
    return(
        <>
        <Head>
            <title>Main Campus - Queen's University Accessible Maps</title>
        </Head>
        <Container>
                <Typography component="h1" variant="h1">Main Campus Map</Typography>
                <Link href="/"><Button variant="contained">Back</Button></Link>
        </Container>
        </>
    );
}