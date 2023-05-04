import  {Container}  from '@mui/material';
import {Typography} from '@mui/material';
import {Button} from '@mui/material';
import Link from 'next/link';
import Layout from '../../components/layout';

export default function MainMap() {
    return(
        <Layout title="West Campus - Queen's University Accessible Maps" description="An Accessible West Campus Map View for Queen's University.">
        <Container>
                <Typography component="h1" variant="h1">Main Campus Map</Typography>
                <Link href="/"><Button variant="contained">Back</Button></Link>
        </Container>
        </Layout>
    );
}